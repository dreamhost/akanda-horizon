TEST_CHOICE = (
    (0, 'Test'),
)

PROTOCOL_CHOICES = (
    (0, 'TCP'),
    (1, 'UDP'),
    (2, 'TCP+UDP'),
)

NEW_PROTOCOL_CHOICES = (
    ('tcp', 'TCP'),
    ('udp', 'UDP'),
    ('tcp+udp', 'TCP+UDP'),
)

NEW_PROTOCOL_CHOICES_DICT = dict(NEW_PROTOCOL_CHOICES)

POLICY_CHOICES = (
    ('pass', 'Allow'),
    ('block', 'Deny'),
)

POLICY_CHOICES_DICT = dict(POLICY_CHOICES)
