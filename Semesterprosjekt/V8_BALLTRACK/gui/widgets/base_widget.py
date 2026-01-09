"""
base_widget.py
---------------------------------------
Felles baseklasse for alle widgets i Balltrack Pi GUI-systemet.

Formål:
    Gi en standardisert struktur og et felles API for alle widgets.
    Sikre at hver widget kan kobles til PositionController gjennom
    en konsistent bind()-metode.

Brukes av:
    Alle widgets i gui/widgets/*

Kalles når:
    BalltrackApp initialiserer GUI og knytter widgets til controlleren.

Ansvar:
    - Oppbevare referanse til controller
    - Tilby felles funksjonalitet for fremtidige behov
      (logging, feilhåndtering, dataformat, osv.)

Relasjoner:
    - PositionController (kontrollerobjekt)
"""

class BaseWidget:
    """
    BaseWidget
    -----------------------------------
    Superklasse for alle widgets.

    Widgets som arver fra BaseWidget får automatisk:
        - felles bind(controller)-metode
        - en sikker plass å legge felles funksjoner senere
    """

    def __init__(self):
        self.controller = None  # Blir satt via bind()

    def bind(self, controller):
        """
        Knytt widgeten til en controller-instans.

        Parametere:
            controller: PositionController
                Objektet som styrer logikk, PID, servo og sensorlesing.

        Kalles av:
            BalltrackApp i main_window.py
        """
        self.controller = controller
