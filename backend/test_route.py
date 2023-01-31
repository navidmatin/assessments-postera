from app.internals.models.route import Route
import json
import pytest


def parse_route_info_will_parse_route_info_correctly():
    input = """{
        "score": 0.0,
        "molecules": [
            {
                "smiles": "O=C(Cn1nnc2ccccc21)N(Cc1ccsc1)c1ccc(Cl)cc1",
                "catalog_entries": [],
                "is_building_block": false
            },
            {
                "smiles": "COC(=O)Cn1nnc2ccccc21",
                "catalog_entries": [
                    {
                        "vendor_id": "MolPort-002-492-362",
                        "catalog_name": "molport",
                        "lead_time_weeks": 0.0
                    },
                    {
                        "vendor_id": "4340565",
                        "catalog_name": "emolecules",
                        "lead_time_weeks": 0.7
                    },
                    {
                        "vendor_id": "MCULE-7236067687",
                        "catalog_name": "mcule",
                        "lead_time_weeks": 5.0
                    },
                    {
                        "vendor_id": "313449",
                        "catalog_name": "pubchem",
                        "lead_time_weeks": 12.0
                    },
                    {
                        "vendor_id": "BBV-2156454",
                        "catalog_name": "enamine_made",
                        "lead_time_weeks": 6.0
                    },
                    {
                        "vendor_id": "s_7____128806____5534970",
                        "catalog_name": "enamine_real",
                        "lead_time_weeks": 4.0
                    }
                ],
                "is_building_block": true
            },
            {
                "smiles": "Clc1ccc(NCc2ccsc2)cc1",
                "catalog_entries": [
                    {
                        "vendor_id": "3162059",
                        "catalog_name": "pubchem",
                        "lead_time_weeks": 12.0
                    },
                    {
                        "vendor_id": "BBV-131088",
                        "catalog_name": "enamine_made",
                        "lead_time_weeks": 6.0
                    },
                    {
                        "vendor_id": "1536185",
                        "catalog_name": "emolecules",
                        "lead_time_weeks": 12.0
                    },
                    {
                        "vendor_id": "EN300-161145",
                        "catalog_name": "enamine_bb",
                        "lead_time_weeks": 12.0
                    },
                    {
                        "vendor_id": "s_38____56070____13230996",
                        "catalog_name": "enamine_real",
                        "lead_time_weeks": 4.0
                    },
                    {
                        "vendor_id": "MolPort-046-846-280",
                        "catalog_name": "molport",
                        "lead_time_weeks": 0.0
                    },
                    {
                        "vendor_id": "MCULE-3563800686",
                        "catalog_name": "mcule",
                        "lead_time_weeks": 0.0
                    }
                ],
                "is_building_block": true
            }
        ],
        "reactions": [
            {
                "name": "Ester amidation",
                "target": "O=C(Cn1nnc2ccccc21)N(Cc1ccsc1)c1ccc(Cl)cc1",
                "sources": [
                    "COC(=O)Cn1nnc2ccccc21",
                    "Clc1ccc(NCc2ccsc2)cc1"
                ],
                "smartsTemplate": "[c,C:1][C:2](=[O:3])[N:4]>>([*:1][C:2](=[O:3])[O]C.[N:4][#1])"
            }
        ],
        "disconnections": {
            "rxns": [
                {
                    "atms": [
                        1,
                        12
                    ],
                    "bnds": [
                        11
                    ],
                    "p_smi": "O=C(Cn1nnc2ccccc21)N(Cc1ccsc1)c1ccc(Cl)cc1"
                }
            ],
            "route": {
                "atms": [
                    [
                        1,
                        12
                    ]
                ],
                "bnds": [
                    [
                        11
                    ]
                ]
            }
        }
    }"""
    route_info = json.loads(input)
    route = Route()
    route.parse_route_info(route_info)
    print(route)
