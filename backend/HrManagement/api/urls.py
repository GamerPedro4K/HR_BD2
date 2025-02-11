from rest_framework.routers import DefaultRouter
from .routes.employees.views import EmployeeViewSet
from .routes.attendance.views import AttendanceViewSet
from .routes.schedule.views import ScheduleViewSet
from .routes.extra_hours.views import ExtraHoursViewSet
from .routes.certificate_type.views import CertificateTypeViewSet
from .routes.payment_methods.views import PaymentMethodViewSet
from .routes.training_types.views import TrainingTypeViewSet
from .routes.type_benefit.views import TypeBenefitViewSet
from .routes.contract_state.views import ContractStateViewSet
from .routes.contract_leave_type.views import ContractLeaveTypeViewSet
from .routes.departments.views import DepartmentViewSet
from .routes.contract_type.views import ContractTypeViewSet
from .routes.vacations.views import VacationsViewSet
from .routes.user_permissions.views import UserPermissionsViewSet
from .routes.absence_reason.views import AbsenceReasonViewSet
from .routes.salary_history.views import SalaryHistoryViewSet
from .routes.deductions.views import DeductionsViewSet
from .routes.bonuses.views import BonusesViewSet
from .routes.payments.views import PaymentsViewSet
from .routes.roles.views import RolesViewSet
from .routes.contract_state_contract.views import ContractStateContractViewSet
from .routes.auth_groups.views import AuthGroupViewSet
from .routes.permissions.views import PermissionsViewSet
from .routes.analytics.views import AnalyticsViewSet
from .routes.group_permissions_user.views import GroupPermissionsViewUserSet

router = DefaultRouter()
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'contract_state_contracts', ContractStateContractViewSet, basename='contract_state_contract')
router.register(r'payments', PaymentsViewSet, basename='payments')
router.register(r'bonuses', BonusesViewSet, basename='bonuses')
router.register(r'deductions', DeductionsViewSet, basename='deductions')
router.register(r'salary_history', SalaryHistoryViewSet, basename='salary_history')	
router.register(r'absence_reason', AbsenceReasonViewSet, basename='absence_reason')
router.register(r'vacations', VacationsViewSet, basename='vacation')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'schedule', ScheduleViewSet, basename='schedule')
router.register(r'extra_hours', ExtraHoursViewSet, basename='extra_hours')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'certificate_types', CertificateTypeViewSet, basename='certificate_type')
router.register(r'payment_methods', PaymentMethodViewSet, basename='payment_method')
router.register(r'training_types', TrainingTypeViewSet, basename='training_type')
router.register(r'type_benefits', TypeBenefitViewSet, basename='type_benefit')
router.register(r'contract_states', ContractStateViewSet, basename='contract_state')
router.register(r'contract_leave_types', ContractLeaveTypeViewSet, basename='contract_leave_type')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'contract_types', ContractTypeViewSet, basename='contract_type')
router.register(r'user_permissions', UserPermissionsViewSet, basename='user_permissions')
router.register(r'roles', RolesViewSet, basename='roles')
router.register(r'authgroup', AuthGroupViewSet, basename='authgroup')
router.register(r'permissions', PermissionsViewSet, basename='permissions')
router.register(r'permissions_user_group', GroupPermissionsViewUserSet, basename='permissions_user_group')

urlpatterns = router.urls
