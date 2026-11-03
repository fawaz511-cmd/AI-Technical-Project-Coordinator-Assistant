import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="IoT Deployment Project Coordinator", layout="wide")

st.title("🚛 AI-Powered IoT Deployment & Project Coordinator Assistant")
st.caption("Managing 200-Truck Telematics Rollout: Milestones, Risk Mitigation, Meeting Summaries, and Client Reporting.")

# Ensure data directory exists
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
csv_path = DATA_DIR / "project_tasks.csv"

# Initialize default task data if file doesn't exist
if not csv_path.exists():
    default_data = {
        "task_id": ["TSK-101", "TSK-102", "TSK-103", "TSK-104", "TSK-105"],
        "task_name": [
            "Procure 200 cellular & SC1000 satellite units",
            "Customs clearance at Jebel Ali Port",
            "Schedule technician bay slots (Dubai Depot)",
            "Install hardware on Fleet Batch A (Trucks 1-100)",
            "Client sign-off and functional testing"
        ],
        "phase": ["Procurement", "Procurement", "Installation", "Installation", "Commissioning"],
        "assigned_to": ["Supply Chain Team", "Logistics Coordinator", "Field Ops Lead", "Field Tech Team A", "Project Coordinator"],
        "target_date": ["2026-03-01", "2026-03-08", "2026-03-12", "2026-03-25", "2026-04-05"],
        "status": ["Completed", "In Progress", "Pending", "Pending", "Pending"],
        "risk_level": ["Low", "Medium", "Low", "High", "Low"]
    }
    pd.DataFrame(default_data).to_csv(csv_path, index=False)

df_tasks = pd.read_csv(csv_path)

# Navigation Tabs matching the 6 requirements
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Task & Milestone Tracker", 
    "🤖 AI Plan & Risk Generator", 
    "📝 Meeting Notes Summarizer", 
    "✉️ Client Email Drafts", 
    "📈 Weekly Status Report"
])

# --- TAB 1: TASK & MILESTONE TRACKER ---
with tab1:
    st.subheader("📋 200-Truck UAE Deployment Task Manager (Excel / Jira View)")
    st.markdown("Track hardware procurement, installation schedules, technician assignments, and commissioning milestones.")
    
    # Editable DataFrame acting like Excel/Jira
    edited_df = st.data_editor(df_tasks, use_container_width=True, num_rows="dynamic")
    
    if st.button("Save Task Updates"):
        edited_df.to_csv(csv_path, index=False)
        st.success("Task tracker updated and saved successfully!")

# --- TAB 2: AI PLAN & RISK GENERATOR ---
with tab2:
    st.subheader("🤖 AI Project Plan & Risk Analyzer")
    st.markdown("Enter a new deployment scope or challenge to automatically generate a structured project breakdown and risk mitigation strategy.")
    
    project_prompt = st.text_area(
        "Describe Project Scope or Bottleneck:", 
        "We need to deploy tracking hardware across 200 refrigerated trucks in Dubai within 6 weeks, but customs clearance at Jebel Ali Port is delayed by 5 days."
    )
    
    if st.button("Generate AI Project Breakdown & Risks"):
        st.info("### 🚀 Generated AI Project Plan & Milestone Breakdown:")
        st.markdown("""
        * **Phase 1: Expedited Procurement & Staging (Days 1–10)**
          * Audit current local warehouse inventory to bypass immediate port bottleneck.
          * File fast-track clearance documentation with Dubai customs.
        * **Phase 2: Staggered Bay Installation (Days 11–30)**
          * Split the 200 trucks into two batches of 100 to optimize technician shifts at the Dubai depot.
          * Deploy cellular units for urban delivery trucks and SC1000 satellite units for cross-border long-haul units.
        * **Phase 3: Testing & Handover (Days 31–42)**
          * Conduct live GPS ping tests and temperature calibration checks before client sign-off.
        """)
        
        st.markdown("### ⚠️ Identified Project Risks & Mitigations:")
        st.error("**High Risk:** Customs delay impacting installation start date.")
        st.markdown("""
        * **Mitigation Strategy:** Reallocate 30 units currently in local buffer stock to kick off Batch A installations immediately while secondary shipments clear port customs. Avoids total schedule stoppage.
        """)

# --- TAB 3: MEETING NOTES SUMMARIZER ---
with tab3:
    st.subheader("📝 Meeting Notes to Action Items Summarizer")
    st.markdown("Paste rough, messy meeting notes from client calls or internal tech syncs to instantly extract clean action items and owners.")
    
    raw_notes = st.text_area(
        "Paste Raw Meeting Notes Here:",
        "Met with Al-Futtaim logistics manager today. They asked if the tracking dashboard can show real-time driver dwell time at the port. John said he will check with the API team. Also, Sarah mentioned that technician bay 3 is booked out next Tuesday, so we need to shift Truck batch 2 schedule. Deadline is still April 5th."
    )
    
    if st.button("Summarize Into Action Items"):
        st.success("### ✅ Extracted Action Items & Assignees:")
        st.markdown("""
        1. **Task:** Investigate API capability for real-time driver dwell time at port.
           * **Assignee:** John
           * **Priority:** Medium
        2. **Task:** Reschedule Truck Batch 2 installation to avoid technician bay 3 conflict on Tuesday.
           * **Assignee:** Technical Project Coordinator (Self)
           * **Priority:** High (Schedule Critical)
        3. **Task:** Confirm April 5th milestone deadline constraints with client stakeholders.
           * **Assignee:** Project Coordinator
           * **Priority:** Low
        """)

# --- TAB 4: CLIENT EMAIL DRAFTS ---
with tab4:
    st.subheader("✉️ Professional Customer Progress Email Generator")
    
    client_name = st.text_input("Client Organization Name:", "Al-Futtaim Logistics Dubai")
    email_tone = st.selectbox("Tone:", ["Professional & Reassuring", "Urgent / Action Required", "Milestone Celebration"])
    update_details = st.text_area("Key Updates to Communicate:", "Batch 1 hardware has arrived at the Dubai depot. Installation scheduled to begin on schedule next Monday.")
    
    if st.button("Draft Client Email"):
        st.markdown("---")
        st.code(f"""
        Subject: Deployment Update: 200-Truck Telematics Rollout — {client_name}
        
        Dear {client_name} Operations Team,
        
        I hope this message finds you well. 
        
        We are writing to provide you with the latest progress update regarding our ongoing fleet tracking deployment across your vehicles.
        
        **Progress Highlights:**
        - {update_details}
        - Our engineering and field tech teams remain fully aligned to meet our scheduled target dates.
        
        **Next Steps:**
        - Commencement of bay installations starting next week. 
        - We will share the preliminary test logs upon completion of Batch 1.
        
        Thank you for your continued partnership. Please let us know if you have any questions.
        
        Best regards,
        
        Technical Project Coordinator
        IoT Deployment & Operations Team
        """, language="markdown")

# --- TAB 5: WEEKLY PROJECT STATUS REPORT ---
with tab5:
    st.subheader("📈 Executive Weekly Project Status Report")
    
    if st.button("Generate Weekly Status Report"):
        completed_count = len(df_tasks[df_tasks["status"] == "Completed"])
        in_progress_count = len(df_tasks[df_tasks["status"] == "In Progress"])
        pending_count = len(df_tasks[df_tasks["status"] == "Pending"])
        
        st.markdown("### 📊 Executive Summary Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("Completed Tasks", completed_count)
        col2.metric("In Progress", in_progress_count)
        col3.metric("Pending Tasks", pending_count)
        
        st.markdown("---")
        st.markdown("""
        **Executive Narrative:**
        The 200-truck IoT deployment for our UAE logistics client is progressing steadily through the procurement and preparatory phases. While minor customs review is underway at Jebel Ali Port, local buffer stock has been allocated to ensure zero downtime for upcoming technician installation slots. 
        
        **Project Health Status:** 🟢 **On Track** (Schedule variance under 2%)
        """)