Recent Balls API

This API returns the most recent 6 to 12 ball events from a cricket innings in structured format.

Features:
- Recent ball tracking (6–12 balls)
- Over.ball format
- Striker & bowler details
- Runs & wicket flag
- Human-readable match labels
- Input validation & error handling

How to run locally:
pip install -r requirements.txt
uvicorn main:app --reload

API Endpoint:
GET /recent-balls/{innings_id}?limit=6
