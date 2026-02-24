# HL7 Generator 2000

A hospital HL7v2 message simulator with a web dashboard. Generates realistic HL7v2 messages across 12 message families using configurable clinical workflows, and sends them via MLLP, file, or console output.

Built as a modern replacement for Google's archived [simhospital](https://github.com/google/simhospital), with more message types, YAML-driven workflows, and an interactive web UI.

## Features

- **12 HL7 message families**: ADT, ORM, ORU, RDE, RDS, MDM, DFT, VXU, BAR, SIU, MFN, ACK
- **29 segment builders**: MSH, PID, PV1, PV2, EVN, OBR, OBX, ORC, NK1, IN1, IN2, IN3, GT1, AL1, DG1, RXE, RXD, RXA, RXG, TXA, FT1, SCH, MRG, MFI, MFE, ZPD, AIG, AIL, AIP
- **12 clinical workflows**: ER visits, inpatient admissions, pharmacy orders, vaccinations, and more
- **Web dashboard**: Real-time message feed, patient browser, workflow management, destination config
- **MLLP transport**: Send messages to any HL7 listener (Mirth Connect, Rhapsody, etc.)
- **Realistic data**: Faker-generated patient demographics, LOINC-coded lab results, ICD-10 diagnoses, insurance from 8 carriers
- **YAML configuration**: All workflows, value sets, and settings are YAML files
- **Time-of-day scheduling**: Configurable message rates that vary by time of day
- **Configurable insurance**: IN1/IN2/IN3 segments with plan type, certification, employer data; `insurance_rate` controls what % of patients get coverage
- **Authentication**: Login-protected dashboard with configurable credentials

## Quick Start

### Prerequisites

- Python 3.11 or higher

### Install

```bash
git clone <repo-url>
cd hl7-generator2000
pip install -r requirements.txt
```

### Run

```bash
python -m src
```

Open [http://localhost:8080](http://localhost:8080) in your browser. Default login credentials are `admin` / `admin`.

To auto-start the simulation on launch:

```bash
python -m src --auto-start
```

### Docker

```bash
# Create your .env file with credentials
cp .env.example .env
# Edit .env to set your username and password

docker-compose up --build
```

The dashboard will be available at `http://localhost:8080` and MLLP on port `2575`.

## Configuration

### Main Config (`config/default.yaml`)

```yaml
facility:
  sending_application: "HIS"
  sending_facility: "GENERAL_HOSPITAL"

scheduling:
  default_rate: 5.0  # messages per minute
  time_of_day:
    - start: "08:00"
      end: "17:00"
      rate: 15.0    # peak hours
    - start: "22:00"
      end: "06:00"
      rate: 2.0     # overnight

transport:
  destinations:
    - name: console
      type: console
      enabled: true
    - name: mirth
      type: mllp
      host: 192.168.1.100
      port: 2575
      enabled: true

patient_pool:
  pool_size: 500
  insurance_rate: 0.85  # 0.0-1.0, percentage of patients with insurance

auth:
  username: "admin"
  password: "changeme"

web:
  host: "0.0.0.0"
  port: 8080
```

### Authentication

Credentials can be set in two ways:

**Config file** (for standalone use):
```yaml
# config/default.yaml
auth:
  username: "myuser"
  password: "mypassword"
```

**Environment variables** (for Docker, override config file):
```bash
# .env file or shell environment
HL7GEN_USERNAME=myuser
HL7GEN_PASSWORD=mypassword
```

### Insurance Segments (IN1/IN2/IN3)

Insurance coverage is controlled by `patient_pool.insurance_rate` in the config:

```yaml
patient_pool:
  insurance_rate: 0.85  # 85% of patients get insurance (default)
  # insurance_rate: 0.0   # Disable insurance entirely
  # insurance_rate: 1.0   # All patients get insurance
```

When a patient has insurance, ADT, BAR, and DFT messages include:

| Segment | Content |
|---------|---------|
| **IN1** | Plan ID, company, group number, subscriber ID, plan type (HMO/PPO/EPO/MCR/MCD), effective/expiration dates, policy number, insured relationship |
| **IN2** | Employer info, Medicare/Medicaid IDs, military info (when applicable) |
| **IN3** | Certification number, pre-auth requirements, penalty type (when applicable) |

Insurance data is randomly assigned from 8 carriers: Blue Cross Blue Shield, Aetna, UnitedHealthcare, Cigna, Humana, Kaiser Permanente, Medicaid, and Medicare.

### Destinations

Three destination types are supported:

| Type | Description | Config |
|------|-------------|--------|
| `console` | Print messages to stdout | `type: console` |
| `mllp` | Send via MLLP protocol | `type: mllp`, `host`, `port` |
| `file` | Write to `.hl7` files | `type: file`, `file_path` |

Destinations can also be managed from the web dashboard under the Destinations page.

## Customization

### Adding Workflows

Workflows are YAML files in `config/workflows/`. Each workflow defines a sequence of clinical steps with optional delays, conditions, and repeats.

```yaml
name: my_custom_workflow
description: "Custom clinical scenario"
weight: 1.0  # relative probability of selection
steps:
  - registration:
      patient_class: "O"
      loc: "CLINIC"
  - delay:
      min: "5m"
      max: "15m"
  - lab_order:
      order_profile: "CBC"
      priority: "R"
  - condition:
      probability: 0.3
      if_true:
        - lab_order:
            order_profile: "CMP"
  - delay:
      min: "30m"
      max: "2h"
  - lab_result:
      order_profile: "CBC"
  - discharge: {}
```

**Available step types:**
- `registration` / `admission` - ADT^A04 / ADT^A01
- `discharge` - ADT^A03
- `transfer` - ADT^A02
- `lab_order` - ORM^O01
- `lab_result` - ORU^R01
- `pharmacy_order` - RDE^O11
- `pharmacy_dispense` - RDS^O13
- `vaccination` - VXU^V04
- `document` - MDM^T02
- `billing` - DFT^P03
- `bar` - BAR^P01
- `scheduling` - SIU^S12
- `master_file` - MFN^M01
- `delay` - Wait a random duration
- `condition` - Probabilistic branching
- `repeat` - Repeat steps N times

### Adding Value Sets

Value sets are YAML files in `config/value_sets/` that provide reference data (lab tests, medications, diagnosis codes, etc.). The simulator loads these automatically on startup.

### CLI Options

```
python -m src [options]

Options:
  -c, --config PATH    Path to YAML config file (default: config/default.yaml)
  --auto-start         Start simulation automatically on launch
  --host HOST          Web server bind address (default: 0.0.0.0)
  --port PORT          Web server port (default: 8080)
  --no-web             Disable the web dashboard
```

## Architecture

```
YAML Config + Workflows
        |
   [Scheduler] ---- time-of-day rate control
        |
   [Patient Pool] -- picks from ~500 simulated patients
        |
   [Workflow Engine] -- walks through workflow steps
        |
   [Step Handlers] -- mutates patient state, produces Events
        |
   [Message Factory] -- routes Events to Generators (ADT, ORM, ORU...)
        |
   [Segment Builders] -- builds MSH, PID, PV1, IN1, IN2, IN3, OBX, etc.
        |
   [Message Router] -- sends HL7 via MLLP, file, console, WebSocket
        |
   [Web Dashboard] -- live view + REST API
```

## Project Structure

```
hl7-generator2000/
├── config/
│   ├── default.yaml           # Main configuration
│   ├── workflows/             # Clinical workflow definitions (12 files)
│   └── value_sets/            # Reference data (labs, meds, diagnoses)
├── src/
│   ├── core/                  # Engine, patient, pool, config, clock
│   ├── generators/
│   │   ├── segment_builders/  # One builder per HL7 segment (29 files)
│   │   └── message_types/     # One generator per message family (12 files)
│   ├── workflows/
│   │   └── step_handlers/     # One handler per step type (14 files)
│   ├── transport/             # MLLP, file writer, console writer, router
│   ├── data/                  # Faker provider, clinical data, identifiers
│   ├── web/                   # FastAPI app, auth, WebSocket, routes
│   ├── templates/             # Jinja2 HTML templates
│   └── utils/                 # Helpers, message log, logging config
├── static/                    # CSS, JavaScript
├── tests/                     # 72 tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Testing

```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx
python -m pytest tests/ -v
```

## License

MIT
