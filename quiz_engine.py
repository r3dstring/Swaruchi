import chainlit as cl


async def ask_question(cl):

    questions = cl.user_session.get("questions")
    index = cl.user_session.get("current_index")

    q = questions[index]

    xp = cl.user_session.get("xp")
    streak = cl.user_session.get("streak")

    level = xp // 50 + 1

    progress = int(((index + 1) / 20) * 10)

    bar = "🟩" * progress + "⬜" * (10 - progress)

    text = f"""
# 🏭 Swaruchi

🏆 Level {level}
⭐ XP: {xp}
🔥 Streak: {streak}

{bar}

Question {index+1}/20

{q['question']}
"""

    await cl.Message(
        content=text,
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
            )
        ]
    ).send()


def check_answer(user_answer, q):

    return (
        user_answer.strip().lower()
        ==
        q["answer"].strip().lower()
    )