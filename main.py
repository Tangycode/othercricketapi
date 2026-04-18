from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional

app = FastAPI()

# Sample in-memory ball data (replace with DB in production)
BALL_EVENTS = {
    "innings_1": [
        {"ball_no": 1, "over": 1, "ball": 1, "striker": "A Sharma", "bowler": "K Khan", "runs": 1, "wicket": 0},
        {"ball_no": 2, "over": 1, "ball": 2, "striker": "A Sharma", "bowler": "K Khan", "runs": 4, "wicket": 0},
        {"ball_no": 3, "over": 1, "ball": 3, "striker": "B Kumar", "bowler": "K Khan", "runs": 0, "wicket": 1},
        {"ball_no": 4, "over": 1, "ball": 4, "striker": "C Yadav", "bowler": "K Khan", "runs": 2, "wicket": 0},
        {"ball_no": 5, "over": 1, "ball": 5, "striker": "C Yadav", "bowler": "K Khan", "runs": 6, "wicket": 0},
        {"ball_no": 6, "over": 1, "ball": 6, "striker": "C Yadav", "bowler": "K Khan", "runs": 1, "wicket": 0},
        {"ball_no": 7, "over": 2, "ball": 1, "striker": "D Singh", "bowler": "M Ali", "runs": 0, "wicket": 0},
        {"ball_no": 8, "over": 2, "ball": 2, "striker": "D Singh", "bowler": "M Ali", "runs": 3, "wicket": 0},
        {"ball_no": 9, "over": 2, "ball": 3, "striker": "E Patel", "bowler": "M Ali", "runs": 1, "wicket": 0},
    ]
}


def validate_ball(ball: Dict) -> bool:
    required_fields = ["over", "ball", "striker", "bowler", "runs", "wicket"]
    for field in required_fields:
        if field not in ball:
            return False
    if not isinstance(ball["runs"], int) or ball["runs"] < 0:
        return False
    if ball["wicket"] not in [0, 1]:
        return False
    return True


def build_recent_balls(ball_events: List[Dict], limit: int = 6) -> List[Dict]:
    # Filter invalid data safely
    valid_balls = [b for b in ball_events if validate_ball(b)]

    if not valid_balls:
        raise HTTPException(status_code=400, detail="No valid ball data available")

    # Sort by ball_no to ensure correct order
    valid_balls.sort(key=lambda x: x["ball_no"])

    recent = valid_balls[-limit:]

    result = []
    for b in recent:
        label = (
            f"{b['over']}.{b['ball']} - "
            f"{b['striker']} faced {b['bowler']} "
            f"and scored {b['runs']} run(s)"
        )
        if b["wicket"] == 1:
            label += " (WICKET!)"

        result.append({
            "over_ball": f"{b['over']}.{b['ball']}",
            "striker": b["striker"],
            "bowler": b["bowler"],
            "runs": b["runs"],
            "wicket": b["wicket"],
            "label": label
        })

    return result


@app.get("/recent-balls/{innings_id}")
def get_recent_balls(innings_id: str, limit: Optional[int] = 6):
    if limit < 6 or limit > 12:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 6 and 12 balls"
        )

    if innings_id not in BALL_EVENTS:
        raise HTTPException(status_code=404, detail="Innings not found")

    try:
        result = build_recent_balls(BALL_EVENTS[innings_id], limit)
        return {
            "innings_id": innings_id,
            "recent_balls": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
