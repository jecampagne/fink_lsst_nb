import pandas as pd
from astropy.time import Time

#auteur J.E Campagne 
#1ere version 7th april 26


def mjd_tai_to_iso_utc(mjd_series):
    """
    Convertit une Pandas Series de dates MJD/TAI en Series de dates ISO/UTC.
    """
    # Conversion de la Series MJD/TAI en Time objects avec scale='tai'
    time_objects = Time(mjd_series, format='mjd', scale='tai')

    # Conversion en UTC et extraction en format ISO
    iso_utc_series = pd.Series(time_objects.utc.iso)

    return iso_utc_series

def datestr_iso_utc_to_mjd_tai(datestr):
    """
    Convertit une chaîne ISO/UTC en MJD/TAI.

    Args:
        datestr (str): Chaîne de date au format 'YYYY-MM-DD HH:MM:SS' (UTC).

    Returns:
        float: Date en MJD/TAI.
    """
    if datestr is None:
        return None
    # Conversion de la chaîne ISO/UTC en objet Time avec scale='utc'
    time_obj = Time(datestr, format='iso', scale='utc')

    # Conversion en MJD/TAI
    return time_obj.tai.mjd

def mjd_tai_to_datestr_iso_utc(mjd_tai):
    """
    Convertit une date MJD/TAI en chaîne ISO/UTC.

    Args:
        mjd_tai (float): Date en MJD/TAI.

    Returns:
        str: Chaîne de date au format 'YYYY-MM-DD HH:MM:SS' (UTC).
    """
    if mjd_tai is None:
        return None

    # Conversion de MJD/TAI en objet Time avec scale='tai'
    time_obj = Time(mjd_tai, format='mjd', scale='tai')

    # Conversion en UTC et format ISO
    return time_obj.utc.iso

print("Fonctions de date OK ✓")