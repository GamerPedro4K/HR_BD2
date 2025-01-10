#
#! type_benefit.py
#? python manage.py seed --seeder 11_type_benefit

from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS type_benefit (
    id_type_benefit UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=None):
    benefits = [
        ("Meal Allowance", "Financial support to cover daily meal expenses."),
        ("Health Insurance", "Access to private health insurance or health-related benefits."),
        ("Life Insurance", "Financial coverage in case of the worker's death."),
        ("Transportation Allowance", "Financial assistance for commuting to and from work."),
        ("Professional Training", "Support for professional development and skill-building courses."),
        ("Additional Vacation Days", "Extra days off beyond the legal vacation entitlement."),
        ("Flexible Working Hours", "Option to adjust working hours for a better work-life balance."),
        ("Remote Work", "Opportunity to work from home partially or fully."),
        ("Childcare Support", "Subsidies or agreements with childcare providers."),
        ("Employee Discounts", "Exclusive discounts on products or services from partner companies."),
        ("Pension Plan Contribution", "Employer contributions to the worker's retirement plan."),
        ("Performance Bonuses", "Additional compensation based on individual or team performance."),
        ("Gym Membership Discounts", "Reduced rates or free access to fitness facilities."),
        ("Mental Health Support", "Access to counseling or mental health programs."),
        ("Stock Options", "Opportunities to own shares in the company."),
        ("Relocation Assistance", "Support for employees moving to a new location for work."),
        ("Parental Leave Support", "Additional leave or financial aid for new parents."),
        ("Anniversary Bonuses", "Financial rewards or gifts for work anniversaries."),
        ("Career Mentorship Programs", "Guidance and mentoring for career growth."),
        ("Volunteer Time Off", "Paid time off to engage in community or charity work."),
        ("Tuition Reimbursement", "Support for further education or degree programs."),
        ("On-Site Parking", "Free or subsidized parking at the workplace."),
        ("Free Snacks and Beverages", "Access to complimentary snacks or drinks at the office."),
        ("Wellness Programs", "Initiatives to promote physical and mental well-being."),
        ("Team-Building Events", "Sponsored activities to enhance teamwork and collaboration."),
        ("Housing Allowance", "Financial support for housing or rent costs."),
        ("Long-Service Awards", "Recognition and rewards for employees with long tenures."),
        ("Technology Stipends", "Support for purchasing work-related devices or software."),
    ]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_type_benefit FROM type_benefit;")
        existing_records = cursor.fetchall()

        if not existing_records:
            for name, description in benefits:
                cursor.execute(
                    """
                    INSERT INTO type_benefit (name, description)
                    VALUES (%s, %s);
                    """,
                    [name, description]
                )
            print("Employee benefits successfully added.")
        else:
            print("Benefits are already seeded.")


def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM type_benefit 
                WHERE id_type_benefit IN (
                    SELECT id_type_benefit FROM type_benefit 
                    ORDER BY id_type_benefit ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM type_benefit;")
