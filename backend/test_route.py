import pytest
from app.internals.models.route import Route
import json
import pdb


def test_parse_route_info_will_parse_route_info_correctly():
    input = """    {
        "score": 1.2,
        "molecules": [
            {
                "smiles": "O=C(Cn1nnc2ccccc21)N(Cc1ccsc1)c1ccc(Cl)cc1",
                "catalog_entries": [],
                "is_building_block": false
            },
            {
                "smiles": "Clc1ccc(I)cc1",
                "catalog_entries": [
                    {
                        "vendor_id": "MolPort-000-153-151",
                        "catalog_name": "molport",
                        "lead_time_weeks": 0.0
                    },
                    {
                        "vendor_id": "477526",
                        "catalog_name": "emolecules",
                        "lead_time_weeks": 0.7
                    },
                    {
                        "vendor_id": "SCHEMBL208292",
                        "catalog_name": "surechembl",
                        "lead_time_weeks": 12.0
                    },
                    {
                        "vendor_id": "12510",
                        "catalog_name": "pubchem",
                        "lead_time_weeks": 12.0
                    },
                    {
                        "vendor_id": "EN300-77395",
                        "catalog_name": "enamine_bb",
                        "lead_time_weeks": 0.7
                    },
                    {
                        "vendor_id": "",
                        "catalog_name": "generic",
                        "lead_time_weeks": 2.0
                    },
                    {
                        "vendor_id": "MCULE-3776065149",
                        "catalog_name": "mcule",
                        "lead_time_weeks": 0.0
                    }
                ],
                "is_building_block": true
            },
            {
                "smiles": "O=C(Cn1nnc2ccccc21)NCc1ccsc1",
                "catalog_entries": [
                    {
                        "vendor_id": "122211285",
                        "catalog_name": "pubchem",
                        "lead_time_weeks": 12.0
                    }
                ],
                "is_building_block": false
            },
            {
                "smiles": "NCc1ccsc1",
                "catalog_entries": [
                    {
                        "vendor_id": "SCHEMBL120232",
                        "catalog_name": "surechembl",
                        "lead_time_weeks": 12.0
                    },
                    {
                        "vendor_id": "WXCD01006275",
                        "catalog_name": "wuxi_bb_screening",
                        "lead_time_weeks": 0.0
                    },
                    {
                        "vendor_id": "MolPort-000-140-225",
                        "catalog_name": "molport",
                        "lead_time_weeks": 0.0
                    },
                    {
                        "vendor_id": "",
                        "catalog_name": "generic",
                        "lead_time_weeks": 2.0
                    },
                    {
                        "vendor_id": "MCULE-1358443205",
                        "catalog_name": "mcule",
                        "lead_time_weeks": 0.0
                    },
                    {
                        "vendor_id": "720302",
                        "catalog_name": "emolecules",
                        "lead_time_weeks": 0.7
                    },
                    {
                        "vendor_id": "4328338",
                        "catalog_name": "pubchem",
                        "lead_time_weeks": 12.0
                    },
                    {
                        "vendor_id": "EN300-110525",
                        "catalog_name": "enamine_bb",
                        "lead_time_weeks": 1.4
                    }
                ],
                "is_building_block": true
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
            }
        ],
        "reactions": [
            {
                "name": "Ester amidation",
                "target": "O=C(Cn1nnc2ccccc21)NCc1ccsc1",
                "sources": [
                    "NCc1ccsc1",
                    "COC(=O)Cn1nnc2ccccc21"
                ],
                "smartsTemplate": "[c,C:1][C:2](=[O:3])[N:4]>>([*:1][C:2](=[O:3])[O]C.[N:4][#1])"
            },
            {
                "name": "Buchwald-Hartwig amination with amide",
                "target": "O=C(Cn1nnc2ccccc21)N(Cc1ccsc1)c1ccc(Cl)cc1",
                "sources": [
                    "Clc1ccc(I)cc1",
                    "O=C(Cn1nnc2ccccc21)NCc1ccsc1"
                ],
                "smartsTemplate": "[c:1][NX3;$(NC=O):2]>>([c:1][I].[N:2][#1])"
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
                    "p_smi": "O=C(Cn1nnc2ccccc21)NCc1ccsc1"
                },
                {
                    "atms": [
                        19,
                        12
                    ],
                    "bnds": [
                        18
                    ],
                    "p_smi": "O=C(Cn1nnc2ccccc21)N(Cc1ccsc1)c1ccc(Cl)cc1"
                }
            ],
            "route": {
                "atms": [
                    [
                        1,
                        12
                    ],
                    [
                        19,
                        12
                    ]
                ],
                "bnds": [
                    [
                        11
                    ],
                    [
                        18
                    ]
                ]
            }
        }
    }"""
    route_info = json.loads(input)
    route = Route()
    route.parse_route_info(route_info)
    assert route.resulting_molecule == "O=C(Cn1nnc2ccccc21)N(Cc1ccsc1)c1ccc(Cl)cc1"
    assert route.score == 1.2
    assert len(route.smiles_to_molecules) == 5
    assert len(
        route.smiles_to_molecules["O=C(Cn1nnc2ccccc21)NCc1ccsc1"].creation_reactions) == 1
    assert len(
        route.smiles_to_molecules["O=C(Cn1nnc2ccccc21)N(Cc1ccsc1)c1ccc(Cl)cc1"].creation_reactions) == 1
