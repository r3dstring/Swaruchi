import chainlit as cl

from pdf_utils import extract_pdf, chunk_text
from groq_utils import generate_questions


def check_answer(user_answer, q):

    return (
        user_answer.strip().lower()
        ==
        q["answer"].strip().lower()
    )


async def ask_question():

    questions = cl.user_session.get("questions")
    index = cl.user_session.get("current_index")

    q = questions[index]

    xp = cl.user_session.get("xp")
    streak = cl.user_session.get("streak")

    level = xp // 50 + 1

    progress = int(((index + 1) / 20) * 10)

    bar = "🟩" * progress + "⬜" * (10 - progress)

    await cl.Message(
        content=f"""
# 🏭 Swaruchi

🏆 Level {level}
⭐ XP: {xp}
🔥 Streak: {streak}

{bar}

Question {index + 1}/20

{q['question']}
""",
        actions=[
            cl.Action(
                name="answer",
                payload={"answer": "A"},
                label=f"A) {q['options'][0]}"
            ),
            cl.Action(
                name="answer",
                payload={"answer": "B"},
                label=f"B) {q['options'][1]}"
            ),
            cl.Action(
                name="answer",
                payload={"answer": "C"},
                label=f"C) {q['options'][2]}"
            ),
            cl.Action(
                name="answer",
                payload={"answer": "D"},
                label=f"D) {q['options'][3]}"
            ),
        ]
    ).send()


async def process_answer(answer):

    questions = cl.user_session.get("questions")
    index = cl.user_session.get("current_index")

    q = questions[index]

    option_map = {
        "A": q["options"][0],
        "B": q["options"][1],
        "C": q["options"][2],
        "D": q["options"][3]
    }

    user_answer = option_map[answer]

    correct = check_answer(
        user_answer,
        q
    )

    xp = cl.user_session.get("xp")
    streak = cl.user_session.get("streak")

    if correct:

        xp += 10
        streak += 1

        cl.user_session.set("xp", xp)
        cl.user_session.set("streak", streak)

        await cl.Message(
            content=f"""
✅ Correct!

+10 XP

{q['explanation']}
"""
        ).send()

    else:

        streak = 0

        cl.user_session.set(
            "streak",
            streak
        )

        await cl.Message(
            content=f"""
❌ Incorrect

Correct Answer:
{q['answer']}

{q['explanation']}
"""
        ).send()

    index += 1

    cl.user_session.set(
        "current_index",
        index
    )

    if index >= len(questions):

        final_xp = cl.user_session.get("xp")

        await cl.Message(
            content=f"""
🏆 LESSON COMPLETE

⭐ Final XP: {final_xp}

🔥 Thanks for learning with Swaruchi!
"""
        ).send()

        return

    await ask_question()


@cl.action_callback("answer")
async def answer_callback(action):

    answer = action.payload["answer"]

    await process_answer(answer)


@cl.on_chat_start
async def start():

    files = await cl.AskFileMessage(
        content="""
# 🏭 Swaruchi

Learn refinery processes through bite-sized challenges.

🔥 Build streaks
⭐ Earn XP
🏆 Unlock levels

Upload a PDF to begin.
""",
        accept=["application/pdf"],
        max_size_mb=50,
        timeout=300
    ).send()

    if not files:

        await cl.Message(
            content="No PDF uploaded."
        ).send()

        return

    pdf = files[0]

    await cl.Message(
        content="⏳ Processing PDF..."
    ).send()

    text = extract_pdf(
        pdf.path
    )

    chunks = chunk_text(text)

    questions = []

    for chunk in chunks:

        try:

            generated = generate_questions(
                chunk
            )

            questions.extend(
                generated
            )

            if len(questions) >= 20:
                break

        except Exception as e:

            print(
                f"Generation error: {e}"
            )

    questions = questions[:20]

    if len(questions) == 0:

        await cl.Message(
            content="No questions generated."
        ).send()

        return

    cl.user_session.set(
        "questions",
        questions
    )

    cl.user_session.set(
        "current_index",
        0
    )

    cl.user_session.set(
        "xp",
        0
    )

    cl.user_session.set(
        "streak",
        0
    )

    await cl.Message(
        content=f"""
✅ Generated {len(questions)} questions.

Let's begin!
"""
    ).send()

    await ask_question()


@cl.on_message
async def main(message):

    await cl.Message(
        content="Please use the answer buttons below the question."
    ).send()
