"""Exam routers — question_bank, exam_paper, session, submission, results, test_series, leaderboard."""
from fastapi import APIRouter
from api.modules.question_bank.router import router as qb_router
from api.modules.exam_paper.router import router as paper_router
from api.modules.exam_session.router import router as session_router
from api.modules.exam_submission.router import router as submission_router
from api.modules.results.router import router as results_router
from api.modules.test_series.router import router as test_series_router
from api.modules.leaderboard.router import router as leaderboard_router

router = APIRouter()
router.include_router(qb_router, prefix="/question-bank", tags=["exam"])
router.include_router(paper_router, prefix="/exam-papers", tags=["exam"])
router.include_router(session_router, prefix="/exam-sessions", tags=["exam"])
router.include_router(submission_router, prefix="/exam-submissions", tags=["exam"])
router.include_router(results_router, prefix="/results", tags=["exam"])
router.include_router(test_series_router, prefix="/test-series", tags=["exam"])
router.include_router(leaderboard_router, prefix="/leaderboard", tags=["exam"])
