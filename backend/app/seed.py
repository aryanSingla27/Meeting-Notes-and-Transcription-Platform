from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import Meeting, Participant, TranscriptSegment, Summary, ActionItem

SAMPLES = [
    ("Q4 Product Strategy", 42, ["Arjun Mehta", "Sarah Chen", "Mike Patel", "Nina Rao"], [
        ("Arjun Mehta", 0, 9, "Thanks everyone. Today I want us to align on the Q4 product strategy and the launch sequence."),
        ("Sarah Chen", 9, 18, "The biggest opportunity is retention. We should prioritize the onboarding redesign before adding more features."),
        ("Mike Patel", 18, 27, "Engineering can support that. The redesign needs about two sprints if the scope stays focused."),
        ("Nina Rao", 27, 35, "From marketing, we can prepare the lifecycle campaign alongside the beta rollout."),
        ("Arjun Mehta", 35, 42, "Great. Let's lock the beta for the first week of November and review metrics every Friday."),
    ], "The team aligned on a Q4 product strategy centered on retention, onboarding, and a focused beta launch.", ["Q4 roadmap", "Onboarding redesign", "Retention", "Beta launch"], ["Prioritize onboarding redesign", "Run a November beta", "Review retention metrics weekly"]),
    ("Weekly Engineering Sync", 31, ["Mike Patel", "Priya Shah", "Daniel Kim"], [
        ("Mike Patel", 0, 8, "Let's go through blockers first. The API migration is the only item at risk."),
        ("Priya Shah", 8, 16, "The migration is working in staging. I need one more review of the authentication changes."),
        ("Daniel Kim", 16, 24, "I'll review the auth PR today and add integration coverage for the new endpoints."),
        ("Mike Patel", 24, 31, "Perfect. If tests stay green, we'll deploy the migration on Thursday morning."),
    ], "Engineering is on track except for final review and test coverage on the API migration.", ["API migration", "Authentication", "Testing"], ["Review authentication PR", "Add integration tests", "Deploy Thursday"]),
    ("Client Discovery Call", 54, ["Sarah Chen", "David Wilson", "Arjun Mehta"], [
        ("Sarah Chen", 0, 11, "Could you walk us through your current reporting workflow?"),
        ("David Wilson", 11, 23, "Our teams spend several hours every week combining reports from three different systems."),
        ("Arjun Mehta", 23, 34, "So automated consolidation and a single dashboard would be the highest-value outcome."),
        ("David Wilson", 34, 45, "Yes, especially if managers can export the same data for quarterly reviews."),
        ("Sarah Chen", 45, 54, "We'll send a proposed workflow and sample dashboard by Friday."),
    ], "The client needs automated reporting consolidation, a unified dashboard, and exportable quarterly reports.", ["Reporting workflow", "Dashboard", "Data export"], ["Send proposed workflow", "Share sample dashboard", "Confirm export requirements"]),
    ("Marketing Planning", 38, ["Nina Rao", "Leah Martin", "Sam Ortiz"], [
        ("Nina Rao", 0, 9, "Our launch campaign should have one clear message across email, social, and the website."),
        ("Leah Martin", 9, 18, "I can create the email sequence and coordinate the landing page copy."),
        ("Sam Ortiz", 18, 28, "I'll prepare the social calendar and three short product videos."),
        ("Nina Rao", 28, 38, "Let's review everything Tuesday and schedule the campaign for the following Monday."),
    ], "Marketing agreed on a unified launch message with coordinated email, web, social, and video assets.", ["Launch campaign", "Email sequence", "Social calendar"], ["Create email sequence", "Prepare social calendar", "Review assets Tuesday"]),
    ("Hiring Calibration", 27, ["Arjun Mehta", "Priya Shah", "Jordan Lee"], [
        ("Arjun Mehta", 0, 8, "We need to calibrate the interview loop before the next round of candidates."),
        ("Priya Shah", 8, 17, "The coding round is good, but the system design rubric needs clearer scoring anchors."),
        ("Jordan Lee", 17, 23, "I'll draft examples for strong, average, and weak answers so interviewers can score consistently."),
        ("Arjun Mehta", 23, 27, "Great. We'll review the rubric before Thursday's interviews."),
    ], "The team is refining the interview rubric to improve consistency, particularly for system design evaluation.", ["Interview loop", "System design", "Scoring rubric"], ["Draft scoring examples", "Review rubric before Thursday"]),
    ("Sprint Retrospective", 45, ["Mike Patel", "Sarah Chen", "Nina Rao", "Daniel Kim"], [
        ("Mike Patel", 0, 10, "Let's keep what worked: smaller tickets and earlier QA involvement made this sprint smoother."),
        ("Sarah Chen", 10, 21, "We still had too many last-minute design changes. A design review before sprint planning could help."),
        ("Daniel Kim", 21, 34, "Agreed. I'd also like a shared checklist for release readiness."),
        ("Nina Rao", 34, 45, "I'll schedule a design review and we'll add the checklist to the team workspace."),
    ], "The retrospective identified earlier design reviews and a shared release-readiness checklist as the main improvements.", ["Sprint process", "Design review", "Release readiness"], ["Schedule design review", "Create release checklist"]),
]

def seed(db: Session):
    if db.query(Meeting).count() > 0:
        return
    base = datetime.utcnow()
    for idx, (title, duration, names, segments, overview, topics, outline) in enumerate(SAMPLES):
        meeting = Meeting(title=title, duration=duration, date=base - timedelta(days=idx, hours=idx * 2))
        db.add(meeting); db.flush()
        for name in names:
            db.add(Participant(meeting_id=meeting.id, name=name, email=f"{name.lower().replace(' ', '.')}@example.com"))
        for speaker, start, end, text in segments:
            db.add(TranscriptSegment(meeting_id=meeting.id, speaker=speaker, start_time=start, end_time=end, text=text))
        db.add(Summary(meeting_id=meeting.id, overview=overview, key_topics="\n".join(topics), outline="\n".join(outline)))
        for j, item in enumerate(outline):
            db.add(ActionItem(meeting_id=meeting.id, title=item, description=f"Follow up on: {item.lower()}.", assignee=names[j % len(names)], completed=False))
    db.commit()
