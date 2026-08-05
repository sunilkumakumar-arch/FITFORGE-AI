from .selectors import ReceptionSelector


class ReceptionDashboardService:
    """
    Builds the complete Reception Dashboard
    for a member.
    """

    @staticmethod
    def get_member_dashboard(member_code):

        member = ReceptionSelector.get_member(member_code)

        if not member:
            return {
                "success": False,
                "message": "Member not found."
            }

        member_hub = ReceptionSelector.get_member_hub(member)

        membership = ReceptionSelector.get_active_membership(member)

        attendance = ReceptionSelector.get_today_attendance(member)

        trainer_assignment = ReceptionSelector.get_trainer_assignment(member)

        pt_package = ReceptionSelector.get_pt_package(member)

        return {
            "success": True,
            "member": member,
            "member_hub": member_hub,
            "membership": membership,
            "attendance": attendance,
            "trainer_assignment": trainer_assignment,
            "pt_package": pt_package,
        }


    @staticmethod
    def search_members(query):
        members = ReceptionSelector.search_members(query)

        results = []

        for member in members:
            membership = ReceptionSelector.get_active_membership(member)

            results.append({
                "member_code": member.member_code,
                "name": f"{member.first_name} {member.last_name}",
                "phone": member.phone,
                "membership_status": (
                    membership.status if membership else "Inactive"
                ),
            })

        return {
            "success": True,
            "count": len(results),
            "results": results,
        }