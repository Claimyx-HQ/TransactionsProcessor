
mock_data = {
        "transactions": {
            "system": [
                {
                    "uuid": "9a1d2bbb",
                    "date": "10-01-2023",
                    "description": "gnss wire",
                    "amount": 666,
                },
                {
                    "uuid": "2a44a663",
                    "date": "10-01-2023",
                    "description": "gnss wire",
                    "amount": 169,
                },
                {
                    "uuid": "5fc2e9e9",
                    "date": "10-01-2023",
                    "description": "gen wire",
                    "amount": 69,
                },
                {
                    "uuid": "123acb14",
                    "date": "10-01-2023",
                    "description": "wire",
                    "amount": 50.6,
                },
                {
                    "uuid": "886d467c",
                    "date": "10-01-2023",
                    "description": "gnss wire",
                    "amount": 100,
                },
                {
                    "uuid": "b0ecc5d8",
                    "date": "10-01-2023",
                    "description": "gnss wire",
                    "amount": 7000,
                },
                {
                    "uuid": "fe4c9dd5",
                    "date": "10-01-2023",
                    "description": "gnss wire",
                    "amount": 2805.74,
                },
                {
                    "uuid": "cd7e4f81",
                    "date": "10-01-2023",
                    "description": "gnss wire back up",
                    "amount": 1794.93,
                },
                {
                    "uuid": "b0ecc5d8",
                    "date": "10-01-2023",
                    "description": "gnss wire",
                    "amount": 1500,
                },
                {
                    "uuid": "fe4c9dd5",
                    "date": "10-01-2023",
                    "description": "gnss wire",
                    "amount": 4500,
                },
                {
                    "uuid": "cd7e4f81",
                    "date": "10-01-2023",
                    "description": "gnss wire back up",
                    "amount": 2000,
                }
            ],
            "bank": [
                {
                    "uuid": "33504eb9",
                    "date": "10-02-2023",
                    "description": "Preauthorized Credit",
                    "amount": 3766.0,
                },
                {
                    "uuid": "57206b0b",
                    "date": "10-02-2023",
                    "description": "Preauthorized Credit",
                    "amount": 13684.89,
                },
                {
                    "uuid": "e636c4fe",
                    "date": "10-02-2023",
                    "description": "Preauthorized Credit",
                    "amount": 7150.6,
                },
                {
                    "uuid": "86029ed8",
                    "date": "10-03-2023",
                    "description": "Preauthorized Credit",
                    "amount": 2805.74,
                },
                {
                    "uuid": "efec722d",
                    "date": "10-04-2023",
                    "description": "Preauthorized Credit",
                    "amount": 1794.93,
                },
                {
                    "uuid": "efec722d",
                    "date": "10-04-2023",
                    "description": "Preauthorized Credit",
                    "amount": 8000,
                }
            ],
        },
        "matches": {
            "one_to_one": [2805.74, 1794.93],
            "multi_to_one": {7150.6:[7000,100,50.6], 8000:[2000,4500,1500]},
            "unmatched_system": [666,169,69],
            "unmatched_bank": [13684.89,3766.0],
        },
    }
