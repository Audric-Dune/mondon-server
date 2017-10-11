import binascii


class AutomateCommand:
    """
    Définit une commande qui peut être envoyé à l'automate.
    """
    def __init__(self, description, hex_value):
        """
        Crée une instance de `AutomateCommand`
        :param description: Description de la commande
        :param hex: Commande encodée en hexadécimale
        """
        self.description = description
        self.hex = hex_value
        self.binary = binascii.unhexlify(hex_value)


# Définition de commandes pour l'automate
CONNECT = AutomateCommand('CONNECT', '46494E530000000C000000000000000000000000')
GET_SPEED = AutomateCommand('GET_SPEED', '46494E530000001A000000020000000080000300010000EF00070101B10014000001')
