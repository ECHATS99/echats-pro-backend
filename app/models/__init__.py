"""Point d'import centralisé de tous les modèles SQLAlchemy, requis pour qu'Alembic
détecte l'intégralité des tables lors de l'autogénération des migrations.
"""
from app.models.institution import Institution  # noqa: F401
from app.models.role_permission import Role, Permission, role_permissions, user_roles  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.plan import Plan  # noqa: F401
from app.models.subscription import Subscription  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401

from app.models.track import Track  # noqa: F401
from app.models.course_module import CourseModule  # noqa: F401
from app.models.lesson import Lesson, LessonFile, LessonImage  # noqa: F401
from app.models.quiz import Quiz, Question, Answer  # noqa: F401
from app.models.exercise import Exercise  # noqa: F401
from app.models.flag import Flag, Submission  # noqa: F401
from app.models.progress import UserProgress, XPHistory  # noqa: F401

from app.models.ctf import CTFEvent, CTFCategory, CTFChallenge, CTFSolve  # noqa: F401
from app.models.classroom import Classroom, ClassroomMember, ClassroomAssignment  # noqa: F401

from app.models.badge import Badge, UserBadge  # noqa: F401
from app.models.certificate import Certificate  # noqa: F401
from app.models.mentor import Mentor, MentorSession  # noqa: F401

from app.models.writeup import Writeup, WriteupVote, WriteupFavorite  # noqa: F401
from app.models.forum import ForumTopic, ForumPost, ForumLike, ForumReport  # noqa: F401

from app.models.product import ProductCategory, Product  # noqa: F401
from app.models.order import Order, OrderItem  # noqa: F401
from app.models.payment import Payment  # noqa: F401

from app.models.notification import Notification  # noqa: F401
from app.models.news import NewsArticle  # noqa: F401
from app.models.paraben import ParabenCourse, ParabenProgress, ParabenRevenue  # noqa: F401
from app.models.admin_settings import AdminSetting, FeatureFlag, SystemMessage, MaintenanceWindow  # noqa: F401
from app.models.ia_prompt import IAPrompt  # noqa: F401
from app.models.refresh_session import RefreshSession  # noqa: F401

__all__ = [
    "Institution", "Role", "Permission", "role_permissions", "user_roles", "User",
    "Plan", "Subscription", "AuditLog",
    "Track", "CourseModule", "Lesson", "LessonFile", "LessonImage",
    "Quiz", "Question", "Answer", "Exercise", "Flag", "Submission",
    "UserProgress", "XPHistory",
    "CTFEvent", "CTFCategory", "CTFChallenge", "CTFSolve",
    "Classroom", "ClassroomMember", "ClassroomAssignment",
    "Badge", "UserBadge", "Certificate", "Mentor", "MentorSession",
    "Writeup", "WriteupVote", "WriteupFavorite",
    "ForumTopic", "ForumPost", "ForumLike", "ForumReport",
    "ProductCategory", "Product", "Order", "OrderItem", "Payment",
    "Notification", "NewsArticle",
    "ParabenCourse", "ParabenProgress", "ParabenRevenue",
    "AdminSetting", "FeatureFlag", "SystemMessage", "MaintenanceWindow", "IAPrompt", "RefreshSession",
]
