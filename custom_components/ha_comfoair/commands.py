from .comfoair import ComfoAirCommand, ParseData


# Die Checksumme ergibt sich durch Addition aller Bytes (exklusive Start und Ende) plus 173. Tauch
# der Wert 0x07 doppelt im Datenbereich auf, so wird nur eine 0x07 für die Checksummenberechnung
# benutzt.
# Wenn die Checksumme größer als ein Byte ist, wird das niederwertigste Byte verwendet.
# Beispiel:
# Kommando: 0x00 0x69
# Anzahl: 0x00
# Summe = 0 + 105 + 0 + 173 = 278
# 278 = 0x0116
# Checksumme = 0x16


# fixer Teil am Anfang: b'\x07\xf3\x07\xf0\x00
# fixer Teil am Ende: \x07\x0f


# start: 0x07 0xF0
# Kommando: Siehe Kommandoliste
# Anzahl: Anzahl der folgenden Datenbytes
# Daten: Nutzdaten
# Checksumme: Checksumme die über Kommando-, Anzahl- und Datenbytes gebildet wurde
# Ende: 0x07 0x0F

#                              Anzahl
#           start     kommando  Datn Daten                                                            check ende
# beispiel: 0x07 0xF0 0x00 0x6A 0x0D 0x03 0x14 0x20 0x43 0x41 0x33 0x35 0x30 0x20 0x6C 0x75 0x78 0x65 0x55 0x07 0x0F


SKIPCOMMANDS = ["0x3e","0x3c","0x9c","0xaa"]

class ParseData:
    def __init__(self, name, value, arrayIndex):
        self.name = name
        self.arrayIndex = arrayIndex
        self.value = value

class ComfoAirCommand:
    def __init__(self, title, command, replycommand, parseData=None):
        self.title = title
        self.command = command
        self.replycommand = replycommand
        self.parseData = parseData

QUERYCOMMANDS = [
    ComfoAirCommand(
        title="Query Sensordata",
        command=b"\x07\xf0\x00\x97\x00\x00\x44\x07\x0f",
        # checksum = 0 + 151 + 0 + 0 + 173 = 324 -> 0x144 -> x44
        replycommand="0x98",
        parseData= [
            ParseData(name=ATTR_TEMP_ENTHALPIE, value=-1, arrayIndex=7),
            ParseData(name=ATTR_HUMIDITY, value=-1, arrayIndex=8),
        ]
    ),

    ComfoAirCommand(
        title="Query Stufen",
        command=b"\x07\xf0\x00\xcd\x00\x00\x7e\x07\x0f",
        # checksum = 0 + 205 + 0 + 0 + 173 = 378 -> 0x17A -> 7A
        replycommand="0xce",
        parseData= [
            ParseData(name=ATTR_PERCENT_OUT_AWAY, value=-1, arrayIndex=7),
            ParseData(name=ATTR_PERCENT_OUT_LEVEL1, value=-1, arrayIndex=8),
            ParseData(name=ATTR_PERCENT_OUT_LEVEL2, value=-1, arrayIndex=9),
            ParseData(name=ATTR_PERCENT_OUT_LEVEL3, value=-1, arrayIndex=17),
            ParseData(name=ATTR_PERCENT_IN_AWAY, value=-1, arrayIndex=10),
            ParseData(name=ATTR_PERCENT_IN_LEVEL1, value=-1, arrayIndex=11),
            ParseData(name=ATTR_PERCENT_IN_LEVEL2, value=-1, arrayIndex=12),
            ParseData(name=ATTR_PERCENT_IN_LEVEL3, value=-1, arrayIndex=18),
            ParseData(name=ATTR_PERCENT_OUT, value=-1, arrayIndex=13),
            ParseData(name=ATTR_PERCENT_IN, value=-1, arrayIndex=14),
            ParseData(name=ATTR_CURRENT_STAGE, value=-1, arrayIndex=15),
        ]
    ),

    ComfoAirCommand(
        title="Query Temperature Status",
        command=b"\x07\xf0\x00\x0f\x00\x00\xbc\x07\x0f",
        # checksum = 0 + 15 + 0 + 0 + 173 = 188 -> 0xbc -> bc
        replycommand="0x10",
        parseData= [
            ParseData(name=ATTR_TEMP_OUTSIDE, value=-1, arrayIndex=7),
            ParseData(name=ATTR_TEMP_SUPPLY_AIR, value=-1, arrayIndex=8),
            ParseData(name=ATTR_TEMP_USED_AIR, value=-1, arrayIndex=9),
            ParseData(name=ATTR_TEMP_FORT_AIR, value=-1, arrayIndex=10),
        ]
    ),

    ComfoAirCommand(
        title="Query Bypass Data",
        command=b"\x07\xf0\x00\x0d\x00\x00\xba\x07\x0f",
        # checksum = 0 + 13 + 0 + 0 + 173 = 186 -> 0xBA -> ba
        replycommand="0x0e",
        parseData= [
            ParseData(name=ATTR_BYPASS_STATUS, value=-1, arrayIndex=7),
        ]
    ),

    ComfoAirCommand(
        title="Query FanData",
        command=b"\x07\xf0\x00\x0b\x00\x00\xb8\x07\x0f", 
        # checksum = 0 + 11 + 0 + 0 + 173 = 184 -> 0xB8 -> b8
        replycommand="0x0c",
        parseData= [
            ParseData(name=ATTR_SUPPLY_AIR_PERCENTAGE, value=-1, arrayIndex=7),
            ParseData(name=ATTR_USED_AIR_PERCENTAGE, value=-1, arrayIndex=8),
        ]
        )
]

# "0xce" kommt und sind die Einstellungsdaten - könnte ich noch verarbeiten
# "0xe0" kommt und sind die Status Bypass - könnte ich noch verarbeiten
# "0xe2" kommt und sind die Status Klappe - könnte ich noch verarbeiten
# "0xec" kommt und sind die Enthalpie-Daten - könnte ich noch verarbeiten


ACKNOLAGE_STRING = b"\x07\xf0\x07\xf0"
############# ALL SEND-COMMANDS
LEVEL_COMMAND = [
    ComfoAirCommand(
        title="Set Fan Level 0", 
        # Stufe 0 = 0x00 0x99 NIEDRIG 0x01
        command=b"\x07\xf0\x00\x99\x01\x01\x48\x07\x0f", 
        # checksum = 0 + 153 + 1 + 1 + 173 = 328 -> 0x148 -> x48
        replycommand=ACKNOLAGE_STRING
        ) 
        
    ,
    ComfoAirCommand(
        title="Set Fan Level 1", 
        # Stufe 0 = 0x00 0x99 NIEDRIG 0x02
        command=b"\x07\xf0\x00\x99\x01\x02\x49\x07\x0f",
        # checksum = 0 + 153 + 1 + 2 + 173 = 329 -> 0x149 -> x49
        replycommand=ACKNOLAGE_STRING
        ) 
        
    ,
    ComfoAirCommand(
        title="Set Fan Level 2", 
        # Stufe 0 = 0x00 0x99 NIEDRIG 0x03
        command=b"\x07\xf0\x00\x99\x01\x03\x4a\x07\x0f",
        # fragewert = 0 + 153 + 1 + 3 + 173 = 330 -> 0x14A -> x4a
        replycommand=ACKNOLAGE_STRING
        ) 
        
    ,
    ComfoAirCommand(
        title="Set Fan Level 3", 
        # Stufe 0 = 0x00 0x99 NIEDRIG 0x04
        command=b"\x07\xf0\x00\x99\x01\x04\x4b\x07\x0f",
        # fragewert = 0 + 153 + 1 + 4 + 173 = 331 -> 0x14B -> x4b
        replycommand=ACKNOLAGE_STRING
        ) 
]

