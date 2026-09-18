\# Fleet Incident Analytics — Data Dictionary



\## 1. Project Objective



This project analyzes synthetic fleet incident and telemetry data to answer:



> What factors generate the most incidents in a fleet, and which factors have the greatest impact on operations and resolution time?



The dataset is completely synthetic and does not contain confidential company data.



\---



\## 2. Dataset Scope



The initial dataset will contain approximately:



\- 500 vehicles

\- 10 plants

\- 10 incident types

\- 5 error codes

\- 4 carriers

\- 3 GPS providers

\- 3 device types

\- Approximately 10,000 incidents



The data will represent fleet operations across Mexico and the United States.



\---



\## 3. Data Model



The project will use a dimensional model / star schema.



\### Fact Table



\- Fact\_Incidents



\### Dimension Tables



\- Dim\_Date

\- Dim\_Vehicle

\- Dim\_Plant

\- Dim\_IncidentType



\---



\# 4. Fact\_Incidents



The Fact\_Incidents table represents individual fleet incidents.



| Column | Description |

|---|---|

| Incident\_ID | Unique identifier for the incident |

| Vehicle\_ID | Vehicle associated with the incident |

| Plant\_ID | Plant associated with the vehicle |

| Incident\_Date | Date when the incident occurred |

| Incident\_Time | Time when the incident occurred |

| Incident\_Type\_ID | Type of incident |

| Error\_Code | Operational error code |

| Severity | Incident severity |

| Status | Current incident status |

| Opened\_DateTime | Date and time when the incident was opened |

| Resolved\_DateTime | Date and time when the incident was resolved |

| GPS\_Provider | GPS provider associated with the vehicle |

| Device\_Type | Tracking device associated with the vehicle |

| Carrier | Communication carrier |

| Technician\_ID | Technician assigned to the incident |



\### Derived Metric



Resolution\_Minutes will be calculated from:



Resolved\_DateTime - Opened\_DateTime



This metric will be used to analyze incident resolution performance.



\---



\# 5. Dim\_Vehicle



The Dim\_Vehicle table contains information about fleet vehicles.



| Column | Description |

|---|---|

| Vehicle\_ID | Unique vehicle identifier |

| Vehicle\_Type | Type of fleet vehicle |

| Model | Vehicle model |

| Year | Vehicle year |

| Active\_Flag | Indicates whether the vehicle is active |



Approximately 500 vehicles will be generated.



Some vehicles will have a higher probability of generating incidents to simulate recurring operational issues.



\---



\# 6. Dim\_Plant



The Dim\_Plant table contains information about operational plants.



| Plant\_ID | Plant\_Name | Region | Country |

|---|---|---|---|

| PLT-5101 | Monterrey Plant | Northeast | Mexico |

| PLT-5176 | Santa Catarina Plant | Northeast | Mexico |

| PLT-5203 | Saltillo Plant | Northeast | Mexico |

| PLT-5288 | Ramos Arizpe Plant | Northeast | Mexico |

| PLT-5355 | Torreon Plant | North | Mexico |

| PLT-5402 | Chihuahua Plant | North | Mexico |

| PLT-6104 | Dallas Plant | South | USA |

| PLT-6207 | Houston Plant | South | USA |

| PLT-6309 | Atlanta Plant | Southeast | USA |

| PLT-6412 | Miami Plant | Southeast | USA |



\---



\# 7. Dim\_IncidentType



The Dim\_IncidentType table defines the incident categories.



| ID | Incident Type | Category |

|---|---|---|

| IT-001 | Communication | Connectivity |

| IT-002 | GPS | Tracking |

| IT-003 | Sensor | Hardware |

| IT-004 | Tablet | Hardware |

| IT-005 | Authentication | Application |

| IT-006 | Synchronization | Data |

| IT-007 | Assignment | Operations |

| IT-008 | Application | Software |

| IT-009 | Hardware | Hardware |

| IT-010 | Carrier | Connectivity |



\---



\# 8. Error Codes



The initial dataset will use five main error codes.



| Error Code | Simulated Meaning |

|---|---|

| CODE\_17 | Token / communication authentication issue |

| CODE\_33 | Credential or retry issue |

| CODE\_50 | Download or synchronization interruption |

| CODE\_71 | Device communication loss |

| CODE\_82 | GPS signal issue |



\---



\# 9. Severity



The dataset will use four severity levels:



\- Low

\- Medium

\- High

\- Critical



Severity will influence the probability of longer resolution times, but it will not determine resolution time automatically.



This introduces variability similar to real operational data.



\---



\# 10. Status



The dataset will use four incident statuses:



\- Open

\- In Progress

\- Resolved

\- Closed



\---



\# 11. Operational Dimensions



\## Carriers



\- Carrier\_A

\- Carrier\_B

\- Carrier\_C

\- Carrier\_D



\## GPS Providers



\- Provider\_A

\- Provider\_B

\- Provider\_C



\## Device Types



\- Tracker\_X

\- Tracker\_Y

\- Tracker\_Z



\---



\# 12. Controlled Patterns



The synthetic dataset will contain controlled relationships so that the analytical process can identify meaningful patterns.



These relationships are intentionally introduced during data generation.



\### Pattern A — Plant



PLT-5176 will have a higher incident volume, particularly involving:



\- Communication

\- GPS



\### Pattern B — Carrier



Carrier\_A will have a higher probability of communication-related incidents.



Communication incidents associated with Carrier\_A will have a higher probability of CODE\_17 and CODE\_71.



\### Pattern C — Resolution Time



CODE\_71 will occur less frequently but will have a higher probability of longer resolution times.



\### Pattern D — Recurring Vehicles



A small percentage of vehicles will have a higher probability of generating incidents.



The objective is to identify recurring vehicles through analysis rather than manually assigning a fixed number of incidents.



\### Pattern E — Frequent vs. High Impact



CODE\_50 will have a relatively high frequency but generally shorter resolution times than CODE\_71.



This will allow the analysis to distinguish between:



\- Most frequent incidents

\- Highest operational impact

\- Longest resolution time



\---



\# 13. Analytical Questions



The dataset should allow the project to answer questions such as:



1\. Which plants have the highest incident volume?

2\. Which incident types occur most frequently?

3\. Which error codes are most common?

4\. Which error codes have the longest average resolution time?

5\. Which vehicles generate recurring incidents?

6\. Which carriers are associated with more communication incidents?

7\. Which GPS providers are associated with more GPS-related incidents?

8\. Which device types have more incidents?

9\. How do incidents change over time?

10\. What percentage of incidents are resolved?

11\. What is the average resolution time?

12\. Which combinations of plant, carrier, device, and error code are associated with higher incident volumes?



\---



\# 14. Important Principle



The synthetic data must contain realistic variability.



Relationships should not be perfectly deterministic.



The purpose is to create a dataset where patterns exist but must be discovered through SQL, Python, and Power BI.



The final analysis should be able to compare:



\- Frequency

\- Severity

\- Resolution time

\- Operational concentration

\- Recurrence

\- Trends over time



\---



\# 15. Technology Stack



The project will use:



\- Python

\- Pandas

\- SQL Server

\- SQL

\- Power BI

\- Git

\- GitHub



\---



\# 16. Data Privacy



All data used in this project will be synthetic.



No confidential, proprietary, personally identifiable, or production data from an employer will be included.

