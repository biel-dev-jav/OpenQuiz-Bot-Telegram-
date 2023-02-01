from telegram import Update, Poll
from telegram.ext import Application, CommandHandler, ContextTypes

import openai

import json

import os

BOT_TOKEN = os.getenv('TELEGRAM-TOKEN')

openai.api_key = os.getenv('OPENAI-TOKEN')

questions = {}


def generate_question(theme):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt="""Make quetions or polls based in prompt
theme: poll
quiz: { 
  "question": "Do you watch more movies or series?",
  "options": ["Movies", "Series", "Both"],
  "multiple_response": false
}

theme: português
quiz: { 
  "question": "A Inteligência Artificial é uma área da tecnologia que visa desenvolver sistemas capazes de realizar tarefas que normalmente requerem inteligência humana, como compreender linguagem natural, tomar decisões complexas e aprender com novos dados. Ela é alimentada por grandes quantidades de dados e algoritmos avançados de aprendizado de máquina, que permitem que os sistemas de IA sejam cada vez mais precisos e úteis. A IA está sendo usada em uma ampla gama de aplicações, desde assistentes virtuais até sistemas de diagnóstico médico e segurança cibernética. É uma tecnologia em rápido desenvolvimento e tem o potencial de transformar a maneira como vivemos, trabalhamos e nos relacionamos uns com os outros.\n\nO que é a Inteligência Artificial?",
  "options": ["Desenvolver robôs humanóides.", "Desenvolver sistemas com inteligência humana.", "Simular inteligência humana para fins de entretenimento.", "Controlar satélites e equipamentos espaciais."],
  "correct": 2
}

theme: history
quiz: {
  "question": "What was the impact of the Industrial Revolution on European society in the 18th and 19th centuries?",
  "options": ["Increase in social and economic inequality.", "Reduction of poverty and increase in prosperity.", "Improvement of living conditions for all social classes.", "Decline of industry and the economy."],
  "correct": 1
}

theme: """ + theme + """
quiz: """,
    temperature=0.9,
    max_tokens=400,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0,
    stop=["theme"])
  return response

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text("""Hi! I am a Telegram bot powered by the powerful OpenAI's GPT-3 model 💡

Use the command "/question topic" to generate unique questions 💬

Challenge your creativity and knowledge with the power of GPT-3 💪

Good luck! 🍀🍀""")

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  command = update.message.text.split(' ')[0]
  theme = update.message.text.replace(command + ' ', '')
  response = generate_question(theme)

  print(response["choices"][0]["text"])
  poll: dict = json.loads(response["choices"][0]["text"])

  if poll.get("correct"):
    await update.message.reply_poll(poll["question"],
                                    poll["options"],
                                    type=Poll.QUIZ,
                                    correct_option_id=poll["correct"] - 1)
  else:
    await update.message.reply_poll(poll["question"],
                                    poll["options"],
                                    allows_multiple_answers=poll.get("multiple_response"))

def main() -> None:
  application = Application.builder().token(BOT_TOKEN).build()

  application.add_handler(CommandHandler('question', question))
  application.add_handler(CommandHandler('start', start))

  application.run_polling()


if __name__ == "__main__":
  main()
