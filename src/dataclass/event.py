
from dataclasses import dataclass, field
from src.dataclass.color import Color
from datetime import date

@dataclass
class Event:
    id: int = -1
    name: str = ""
    cancel: bool = False

    # Start et end son en UNIX TIME c'est à dire en secondes à partir de 1/1/1970 UTC, transformable en temps lisible par un humain via ce code:
    """
    from datetime import datetime

    user = User(start=1714233600)  # Exemple de timestamp UNIX
    dt = datetime.fromtimestamp(user.start)

    print(dt)  # format lisible : 2025-04-28 00:00:00
    """
    start: int = 0
    end: int = 0
    color: Color = field(default_factory=lambda: Color(255, 0, 0))
    frequency: str = ""  # 'daily', 'weekly', 'monthly', 'yearly'
    interval: int = 0  # tous les N jours/semaines/mois
    by_day: int = 0  # pour 'weekly' : 1 (lundi), 2 (mardi), 3 (mercredi), 4 (jeudi), 5 (vendredi), 6 (samedi), 7 (dimanche)
    by_month_day: int = 0 # pour 'monthly' : 6 (tous les 6 du mois)
    until: int = 0  # date de fin éventuelle

def matches_date(event: Event, target_date: date) -> bool:
    """
    Détermine si un événement récurrent se produit à une date cible donnée.

    Paramètres :
    -----------
    recurrence : Recurrence

    target_date : date
        La date à vérifier (par exemple, 2025-05-06).

    start_date : date
        La date de départ de la récurrence (date du premier événement).

    Retour :
    --------
    bool :
        True si la récurrence inclut la date cible, False sinon.
    """
    # Check optional end condition
    if event.until and target_date > date.fromtimestamp(event.until):
        return False
    
    start_date = date.fromtimestamp(event.start)
    delta = target_date - start_date

    if event.frequency == 'daily':
        return delta.days >= 0 and (delta.days % event.interval == 0)

    elif event.frequency == 'weekly':
        same_weekday = target_date.isoweekday() == event.by_day
        return delta.days >= 0 and same_weekday and (delta.days // 7) % event.interval == 0

    elif event.frequency == 'monthly':
        same_day = target_date.day == event.by_month_day
        month_diff = (target_date.year - start_date.year) * 12 + (target_date.month - start_date.month)
        return month_diff >= 0 and same_day and (month_diff % event.interval == 0)

    elif event.frequency == 'yearly':
        same_day = target_date.day == event.by_day and target_date.month == event.by_month_day
        year_diff = target_date.year - start_date.year
        return year_diff >= 0 and same_day and (year_diff % event.interval == 0)

    return False
