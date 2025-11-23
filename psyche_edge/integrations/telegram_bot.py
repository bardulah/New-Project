"""
PsycheEdge Telegram Bot
Mobile control interface for the swarm
Commands:
- /status - Swarm status
- /spawn [type] [count] - Spawn agents
- /top - Top agents
- /insights - Recent insights
- /logbet - Log a bet decision
- /logmood - Log mood
- /tilt - Check tilt status
"""
import os
import sys
from pathlib import Path
import logging

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

from psyche_edge.core.swarm import SwarmOrchestrator
from psyche_edge.agents import (
    CialdiniScientist, BiasHunter, TiltDetector,
    DecisionLogger, CodeEvolutor, MetaObserver, SwarmSpawner
)
from psyche_edge.integrations.biometrics import BiometricIntegration
from psyche_edge.experiments.decision_tracker import DecisionTracker

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class PsycheEdgeBot:
    """Telegram bot for PsycheEdge control"""

    def __init__(self):
        self.swarm = None
        self.biometrics = BiometricIntegration()
        self.decision_tracker = DecisionTracker()
        self.user_context = {}  # Store conversation state per user

    def init_swarm(self):
        """Initialize swarm if not already done"""
        if self.swarm is None:
            self.swarm = SwarmOrchestrator(data_dir="psyche_edge/data")

            # Register agents
            self.swarm.register_agent_class("CialdiniScientist", CialdiniScientist)
            self.swarm.register_agent_class("BiasHunter", BiasHunter)
            self.swarm.register_agent_class("TiltDetector", TiltDetector)
            self.swarm.register_agent_class("DecisionLogger", DecisionLogger)
            self.swarm.register_agent_class("CodeEvolutor", CodeEvolutor)
            self.swarm.register_agent_class("MetaObserver", MetaObserver)
            self.swarm.register_agent_class("SwarmSpawner", SwarmSpawner)

            # Spawn initial population if needed
            if len(self.swarm.agents) == 0:
                for _ in range(20):
                    agent_type = ["BiasHunter", "TiltDetector", "CialdiniScientist"][_ % 3]
                    self.swarm.spawn_agent(agent_type)

                # Start swarm
                self.swarm.start_swarm()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command"""
        await update.message.reply_text(
            "🧠 *PsycheEdge 2025*\n\n"
            "Self-Evolving Decision Science Laboratory\n\n"
            "Commands:\n"
            "/status - Swarm status\n"
            "/spawn - Spawn agents\n"
            "/top - Top performers\n"
            "/insights - Recent insights\n"
            "/logbet - Log a bet\n"
            "/logmood - Log mood\n"
            "/tilt - Check tilt\n"
            "/help - Show this message",
            parse_mode='Markdown'
        )

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get swarm status"""
        self.init_swarm()

        state = self.swarm.get_swarm_state()

        status_emoji = "🟢" if self.swarm.running else "🔴"

        message = (
            f"{status_emoji} *Swarm Status*\n\n"
            f"👥 Population: {state['population']}\n"
            f"🐣 Born: {state['total_born']}\n"
            f"💀 Died: {state['total_died']}\n"
            f"🔄 Cycles: {state['cycles']}\n\n"
            f"*Species:*\n"
        )

        for species, count in state['species_count'].items():
            message += f"  • {species}: {count}\n"

        if state['recent_fitness']:
            latest = state['recent_fitness'][-1]
            message += f"\n📈 Avg Fitness: {latest['avg_fitness']:.1f}"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def spawn(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Spawn new agents"""
        self.init_swarm()

        # Parse args: /spawn BiasHunter 5
        args = context.args

        if len(args) >= 2:
            agent_type = args[0]
            count = int(args[1])
        elif len(args) == 1:
            agent_type = args[0]
            count = 1
        else:
            agent_type = "BiasHunter"
            count = 1

        # Spawn
        spawned = []
        for _ in range(count):
            try:
                agent = self.swarm.spawn_agent(agent_type)
                spawned.append(agent)
            except Exception as e:
                await update.message.reply_text(f"❌ Error: {e}")
                return

        await update.message.reply_text(
            f"✅ Spawned {len(spawned)} {agent_type} agents!"
        )

    async def top_agents(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show top agents"""
        self.init_swarm()

        top_agents = self.swarm.get_top_agents(5)

        if not top_agents:
            await update.message.reply_text("No agents yet!")
            return

        message = "🏆 *Top Agents*\n\n"

        for i, agent in enumerate(top_agents, 1):
            message += (
                f"{i}. {agent.agent_type}\n"
                f"   Fitness: {agent.metrics.fitness_score:.1f}\n"
                f"   Gen: {agent.generation}\n\n"
            )

        await update.message.reply_text(message, parse_mode='Markdown')

    async def insights(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show recent insights"""
        self.init_swarm()

        recent_insights = self.swarm.world_state.get('recent_insights', [])[-5:]

        if not recent_insights:
            await update.message.reply_text("No insights yet!")
            return

        message = "💡 *Recent Insights*\n\n"

        for insight in reversed(recent_insights):
            agent_type = insight.get('agent_type', 'Unknown')
            insight_data = insight.get('insight', {})

            message += f"*{agent_type}:*\n"
            message += f"{insight_data}\n\n"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def log_bet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Log a betting decision"""
        user_id = update.effective_user.id

        # Simple flow: ask for bet details
        await update.message.reply_text(
            "🎲 *Log a Bet*\n\n"
            "Send me the details in this format:\n"
            "`sport | bet_type | bet_size | game | reasoning`\n\n"
            "Example:\n"
            "`NBA | spread | 100 | Lakers -5.5 | They're hot`",
            parse_mode='Markdown'
        )

        # Set user context
        self.user_context[user_id] = {'awaiting': 'bet_details'}

    async def log_mood(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Log mood"""
        args = context.args

        if not args:
            await update.message.reply_text(
                "💭 *Log Mood*\n\n"
                "Usage: /logmood [mood] [stress_level]\n\n"
                "Moods: calm, anxious, excited, angry, tired\n"
                "Stress: 1-10\n\n"
                "Example: `/logmood anxious 7`",
                parse_mode='Markdown'
            )
            return

        mood = args[0]
        stress_level = int(args[1]) if len(args) > 1 else 5

        self.biometrics.log_mood(mood, stress_level)

        await update.message.reply_text(f"✅ Mood logged: {mood}, stress={stress_level}")

    async def check_tilt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check tilt status"""
        self.init_swarm()

        # Get biometrics
        biometrics = self.biometrics.get_latest_biometrics()

        # Get recent decisions
        decisions = self.decision_tracker.get_decision_history(limit=10)

        # Simple tilt check
        hrv = biometrics.get('hrv', 60)
        stress = biometrics.get('stress_level', 5)

        tilt_score = (10 - hrv / 10) + stress
        tilt_score = min(10, tilt_score)

        if tilt_score > 7:
            status = "🚨 HIGH TILT"
            advice = "STOP. Take a break. Do not make decisions now."
        elif tilt_score > 5:
            status = "⚠️ MODERATE TILT"
            advice = "Caution advised. Consider taking a break."
        else:
            status = "✅ NO TILT"
            advice = "You're good to go."

        message = (
            f"*Tilt Status*\n\n"
            f"{status}\n"
            f"Score: {tilt_score:.1f}/10\n\n"
            f"📊 *Metrics:*\n"
            f"HRV: {hrv}\n"
            f"Stress: {stress}\n\n"
            f"💡 {advice}"
        )

        await update.message.reply_text(message, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle free-form messages"""
        user_id = update.effective_user.id
        text = update.message.text

        # Check if user is in a flow
        if user_id in self.user_context:
            ctx = self.user_context[user_id]

            if ctx.get('awaiting') == 'bet_details':
                # Parse bet details
                parts = [p.strip() for p in text.split('|')]

                if len(parts) >= 5:
                    import time

                    decision_id = self.decision_tracker.log_betting_decision(
                        sport=parts[0],
                        bet_type=parts[1],
                        bet_size=float(parts[2]),
                        odds=1.91,  # Default
                        expected_value=0,
                        book="unknown",
                        game=parts[3],
                        reasoning=parts[4],
                        timestamp=time.time()
                    )

                    await update.message.reply_text(
                        f"✅ Bet logged!\n"
                        f"ID: {decision_id}\n\n"
                        f"The swarm is analyzing your decision..."
                    )

                    # Clear context
                    del self.user_context[user_id]
                else:
                    await update.message.reply_text(
                        "❌ Invalid format. Please use:\n"
                        "`sport | bet_type | bet_size | game | reasoning`",
                        parse_mode='Markdown'
                    )


def main():
    """Run bot"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set in .env")
        return

    # Create bot instance
    bot = PsycheEdgeBot()

    # Create application
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.start))
    application.add_handler(CommandHandler("status", bot.status))
    application.add_handler(CommandHandler("spawn", bot.spawn))
    application.add_handler(CommandHandler("top", bot.top_agents))
    application.add_handler(CommandHandler("insights", bot.insights))
    application.add_handler(CommandHandler("logbet", bot.log_bet))
    application.add_handler(CommandHandler("logmood", bot.log_mood))
    application.add_handler(CommandHandler("tilt", bot.check_tilt))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))

    # Run bot
    logger.info("🤖 PsycheEdge Telegram Bot starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
