# ARCHITECTURE.MD

```
amleth/
│
├── amleth/                        # Main package
│   ├── __init__.py                # Makes amleth a Python package
│   ├── broker.py                  # MQTT broker integration
│   ├── config.py                  # Access environment variables in a standard way
│   ├── database.py                # SQLite database integration  
│   ├── main.py                    # Entrypoint for the application 
│   ├── mqtt_event_processor.py    # Transforms mqtt event to db record 
│   └── utils.py                   # Utility functions used cross-application 
│
├── tests/                         # Unit tests and integration tests
│   ├── __init__.py
│   └── 
│
│── data/                          # Data files like logs and database
│
├── docs/                          # Documentation files
│
├── scripts/                       # Helpful scripts, e.g., deployment and database initialization 
│
├── requirements.txt               # Project dependencies
├── Dockerfile                     # Container definition
├── README.md                      # Project overview
├── ARCHITECTURE.md                # Project layour overview
├── LICENSE                        # LICENSE 
└── .gitignore                     # Specifies intentionally untracked files to ignore
```