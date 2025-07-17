buffer_arrange_test_case = [
    {
        'name': 'tc_mock_buffer_file_read_as_list',
        'input': [
            ['W', 2, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 6, '0x00000001'],
        ],
        'expected': [
            ['W', 2, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 6, '0x00000001'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_mock_buffer_file_read_as_list',
        'input': [
            ['W', 2, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 6, '0x00000001'],
            ['W', 8, '0x00000001'],
            ['W', 10, '0x00000001'],
        ],
        'expected': [
            ['W', 2, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 6, '0x00000001'],
            ['W', 8, '0x00000001'],
            ['W', 10, '0x00000001'],
        ],
    },
    {
        'name': 'tc_test_buffer_duplicate_write_with_mock',
        'input': [
            ['W', 2, '0x00000001'],
            ['W', 2, '0x00000001'],
            ['W', 2, '0x00000001'],
            ['W', 2, '0x00000001'],
            ['W', 2, '0x00000001'],
            ['W', 2, '0x00000001'],
            ['W', 2, '0x00000001'],
            ['W', 2, '0x00000001'],
            ['W', 2, '0x00000001'],
        ],
        'expected': [
            ['W', 2, '0x00000001'],
            ['empty'],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_duplicate_write_with_mock',
        'input': [
            ['W', 2, '0x00000001'],
            ['W', 3, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 2, '0x00000001'],
            ['W', 3, '0x00000001'],
            ['W', 4, '0x00000001'],
        ],
        'expected': [
            ['W', 2, '0x00000001'],
            ['W', 3, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_duplicate_erase_with_mock',
        'input': [['E', 4, 6], ['E', 4, 6], ['E', 4, 6]],
        'expected': [
            ['E', 4, 6],
            ['empty'],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_duplicate_erase_with_mock',
        'input': [['E', 4, 6], ['E', 5, 3], ['E', 6, 1]],
        'expected': [
            ['E', 4, 6],
            ['empty'],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_write_and_erase_with_mock',
        'input': [
            ['W', 2, '0x00000001'],
            ['W', 3, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 5, '0x00000001'],
            ['E', 2, 4],
        ],
        'expected': [
            ['E', 2, 4],
            ['empty'],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_write_and_erase_with_mock',
        'input': [
            ['W', 2, '0x00000001'],
            ['W', 3, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 5, '0x00000001'],
            ['E', 4, 6],
        ],
        'expected': [
            ['W', 2, '0x00000001'],
            ['W', 3, '0x00000001'],
            ['E', 4, 6],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_erase_and_write_with_mock',
        'input': [
            ['E', 2, 4],
            ['W', 2, '0x00000001'],
            ['W', 3, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 5, '0x00000001'],
        ],
        'expected': [
            ['W', 2, '0x00000001'],
            ['W', 3, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 5, '0x00000001'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_erase_and_write_with_mock',
        'input': [['E', 2, 4], ['W', 3, '0x00000001']],
        'expected': [
            ['E', 2, 4],
            ['W', 3, '0x00000001'],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_erase_and_write_with_mock',
        'input': [['E', 2, 10], ['W', 11, '0x00000001']],
        'expected': [
            ['E', 2, 9],
            ['W', 11, '0x00000001'],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_merge_erase_with_mock',
        'input': [
            ['E', 2, 1],
            ['E', 3, 1],
            ['E', 4, 1],
            ['E', 5, 1],
            ['E', 6, 1],
        ],
        'expected': [
            ['E', 2, 5],
            ['empty'],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_merge_erase_with_mock',
        'input': [
            ['E', 2, 2],
            ['E', 3, 2],
            ['E', 4, 2],
            ['E', 5, 2],
            ['E', 6, 2],
        ],
        'expected': [
            ['E', 2, 6],
            ['empty'],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
]


tc_test_buffer_merge_erase_over_10_with_mock = [
    {
        'name': 'tc_test_buffer_merge_erase_over_10_with_mock',
        'input': [['E', 5, 8], ['E', 10, 8]],
        'expected': [
            ['E', 5, 3],
            ['E', 8, 10],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    }
]


tc_test_buffer_merge_and_merge_erase_with_mock = [
    {
        'name': 'tc_test_buffer_merge_and_merge_erase_with_mock',
        'input': [
            ['E', 0, 3],
            ['E', 6, 3],
            ['E', 3, 3],
        ],
        'expected': [
            ['E', 0, 9],
            ['empty'],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
    {
        'name': 'tc_test_buffer_merge_and_merge_erase_with_mock',
        'input': [['E', 5, 10], ['E', 15, 10], ['E', 10, 10]],
        'expected': [
            ['E', 5, 10],
            ['E', 15, 10],
            ['empty'],
            ['empty'],
            ['empty'],
        ],
    },
]

buffer_read_test_case = [
    {
        'name': 'tc_nothing_to_read_from_buffer',
        'input': [[['empty'], ['empty'], ['empty'], ['empty'], ['empty']], 3],
        'expected': (False, ''),
    },
    {
        'name': 'tc_read_erase_from_buffer',
        'input': [[['E', 3, 3], ['empty'], ['empty'], ['empty'], ['empty']], 3],
        'expected': (True, '0x00000000'),
    },
    {
        'name': 'tc_read_write_from_buffer',
        'input': [
            [['W', 3, '0x00000001'], ['empty'], ['empty'], ['empty'], ['empty']],
            3,
        ],
        'expected': (True, '0x00000001'),
    },
]


tc_test_buffer_is_full_with_mock = [
    {
        'name': 'tc_test_buffer_is_full_with_mock',
        'input': [
            ['W', 2, '0x00000001'],
            ['W', 3, '0x00000001'],
            ['W', 4, '0x00000001'],
            ['W', 5, '0x00000001'],
            ['W', 25, '0x00000001'],
            ['W', 26, '0x00000001'],
            ['W', 28, '0x00000001'],
            ['W', 29, '0x00000001'],
        ],
        'expected': [],
    },
    {
        'name': 'tc_test_buffer_is_full_with_mock',
        'input': [
            ['E', 0, 6],
            ['E', 10, 6],
            ['E', 40, 6],
            ['E', 50, 6],
            ['E', 70, 6],
            ['E', 60, 6],
        ],
        'expected': [],
    },
]
