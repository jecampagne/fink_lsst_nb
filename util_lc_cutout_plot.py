import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import pandas as pd

from util_date import *



FILTER_COLORS = {
    'u': '#7B2FBE',
    'g': '#0077BB',
    'r': '#33AA77',
    'i': '#DDAA33',
    'z': '#BB5500',
    'y': '#AA0000',
}

FILTER_ORDER = ['u', 'g', 'r', 'i', 'z', 'y']

ZP_AB = 2.5 * np.log10(3631e9)   # ≈ 31.4 pour F en nJy


def flux_njy_to_mjy(flux_njy, flux_err_njy):
    """Convertit nJy → mJy."""
    return np.asarray(flux_njy, dtype=float) * 1e-6, \
           np.asarray(flux_err_njy, dtype=float) * 1e-6

def flux_to_mag_ab(flux_njy, flux_err_njy):
    """Flux (nJy) → magnitude AB + erreur propagée. NaN si flux ≤ 0."""
    flux   = np.asarray(flux_njy,     dtype=float)
    flux_e = np.asarray(flux_err_njy, dtype=float)
    valid   = flux > 0
    mag     = np.full(flux.shape, np.nan)
    mag_err = np.full(flux.shape, np.nan)
    mag[valid]     = -2.5 * np.log10(flux[valid]) + ZP_AB
    mag_err[valid] = (2.5 / np.log(10)) * np.abs(flux_e[valid] / flux[valid])
    return mag, mag_err

def flux_mjy_to_mag_ab(flux_mjy, flux_err_mjy):
    """
    Flux (mJy) → magnitude AB + erreur propagée.
    m = -2.5 * log10(F_mJy / 3631e3)  [3631 Jy = 3631e3 mJy]
    NaN si flux ≤ 0.
    """
    flux   = np.asarray(flux_mjy,     dtype=float)
    flux_e = np.asarray(flux_err_mjy, dtype=float)
    valid   = flux > 0
    mag     = np.full(flux.shape, np.nan)
    mag_err = np.full(flux.shape, np.nan)
    mag[valid]     = -2.5 * np.log10(flux[valid] / 3631e3)
    mag_err[valid] = (2.5 / np.log(10)) * np.abs(flux_e[valid] / flux[valid])
    return mag, mag_err



def _prepare_lc(df):
    """Nettoyage commun : conversion types, drop NaN, ajout colonne 'date'."""
    df = df.copy()
    # Conversion des colonnes en numérique
    for col in ['midpointMjdTai', 'psfFlux', 'psfFluxErr']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Suppression des NaN
    df = df.dropna(subset=['midpointMjdTai', 'psfFlux', 'psfFluxErr'])
    # Conversion MJD/TAI -> ISO/UTC pour la colonne 'date'
    date_strings = mjd_tai_to_iso_utc(df['midpointMjdTai'])
    # Conversion explicite en datetime64[ns]
    df['date'] = pd.to_datetime(date_strings, errors='coerce')
    return df

def _apply_date_axis(ax,show_xlabel=True):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    ax.grid(True, alpha=0.2, linewidth=0.5)
    if show_xlabel:
        ax.set_xlabel("Date (UTC)")


def _add_window_band(ax, mjd_start, mjd_end, df):
    """Ajoute une bande verticale semi-transparente pour la fenêtre [START, END]."""
    # Conversion des MJD/TAI en dates ISO/UTC (scalaires)
    t0 = mjd_tai_to_iso_utc([mjd_start]).iloc[0] if mjd_start is not None else None
    t1 = mjd_tai_to_iso_utc([mjd_end]).iloc[0]   if mjd_end   is not None else None

    # Conversion en datetime64[ns] si ce sont des strings
    t0_dt = pd.to_datetime(t0, errors='coerce') if t0 is not None else None
    t1_dt = pd.to_datetime(t1, errors='coerce') if t1 is not None else None

    if t0_dt is not None and t1_dt is not None:
        xmin = t0_dt
        xmax = t1_dt
    elif t0_dt is not None:
        xmin = t0_dt
        xmax = df['date'].max()
    elif t1_dt is not None:
        xmin = df['date'].min()
        xmax = t1_dt
    else:
        return
    ax.axvspan(xmin, xmax, alpha=0.07, color='royalblue')


def plot_flux_mjy(ax, df, obj_id=None, mjd_start=None, mjd_end=None):
    """Courbe de lumière en flux PSF (mJy)."""
    required = {'midpointMjdTai', 'psfFlux', 'psfFluxErr', 'band'}
    if not required.issubset(df.columns):
        ax.text(0.5, 0.5, "Données manquantes", ha='center', va='center',
                transform=ax.transAxes, color='gray')
        return
    df = _prepare_lc(df)
    if df.empty:
        ax.text(0.5, 0.5, "Pas de données valides", ha='center', va='center',
                transform=ax.transAxes, color='gray')
        return

    flux_mjy, ferr_mjy = flux_njy_to_mjy(df['psfFlux'].values, df['psfFluxErr'].values)
    df['flux_mjy'] = flux_mjy
    df['ferr_mjy'] = ferr_mjy

    _add_window_band(ax, mjd_start, mjd_end, df)

    bands = sorted(df['band'].dropna().unique(), 
                   key=lambda x: FILTER_ORDER.index(x) if x in FILTER_ORDER else len(FILTER_ORDER))
    for band in bands:
        sub   = df[df['band'] == band].sort_values('date')
        color = FILTER_COLORS.get(band, '#888888')
        ax.errorbar(sub['date'], sub['flux_mjy'], yerr=sub['ferr_mjy'],
                    fmt='o', color=color, label=f"${band}$",
                    markersize=4, capsize=3, capthick=0.8,
                    elinewidth=0.8, linewidth=0.8, alpha=0.85)
    ax.axhline(0, color='gray', lw=0.6, ls='--', alpha=0.5)
    ax.set_ylabel("Flux PSF (mJy)")
    ax.legend(ncol=len(bands), loc='upper left',
              handlelength=1, handletextpad=0.4, columnspacing=0.6)
    _apply_date_axis(ax)


def plot_mag_ab(ax, df, obj_id=None, mjd_start=None, mjd_end=None):
    """Courbe de lumière en magnitude AB."""
    required = {'midpointMjdTai', 'psfFlux', 'psfFluxErr', 'band'}
    if not required.issubset(df.columns):
        ax.text(0.5, 0.5, "Données manquantes", ha='center', va='center',
                transform=ax.transAxes, color='gray')
        return
    df = _prepare_lc(df)
    if df.empty:
        ax.text(0.5, 0.5, "Pas de données valides", ha='center', va='center',
                transform=ax.transAxes, color='gray')
        return

    flux_mjy, ferr_mjy = flux_njy_to_mjy(df['psfFlux'].values, df['psfFluxErr'].values)
    mag, mag_err = flux_mjy_to_mag_ab(flux_mjy, ferr_mjy)
    df['mag']     = mag
    df['mag_err'] = mag_err

    _add_window_band(ax, mjd_start, mjd_end, df)

    bands = sorted(df['band'].dropna().unique(), 
                   key=lambda x: FILTER_ORDER.index(x) if x in FILTER_ORDER else len(FILTER_ORDER))

    for band in bands:
        sub   = df[df['band'] == band].sort_values('date')
        color = FILTER_COLORS.get(band, '#888888')
        det   = sub.dropna(subset=['mag'])
        if not det.empty:
            ax.errorbar(det['date'], det['mag'], yerr=det['mag_err'],
                        fmt='o', color=color, label=f"${band}$",
                        markersize=4, capsize=3, capthick=0.8,
                        elinewidth=0.8, linewidth=0.8, alpha=0.85)
        nondet = sub[sub['mag'].isna()]
        if not nondet.empty:
            ferr = flux_njy_to_mjy(nondet['psfFluxErr'].values,
                                   nondet['psfFluxErr'].values)[0]
            v    = ferr > 0
            lim  = np.full(ferr.shape, np.nan)
            lim[v] = -2.5 * np.log10(3 * ferr[v] / 3631e3)
            ax.scatter(nondet['date'], lim, marker='v', color=color,
                       s=25, alpha=0.4, zorder=3)
    ax.invert_yaxis()
    ax.set_ylabel("Magnitude AB")
    ax.legend(ncol=len(bands), loc='upper left',
              handlelength=1, handletextpad=0.4, columnspacing=0.6)
    _apply_date_axis(ax)


#for backward compatibility
plot_flux = plot_flux_mjy
plot_mag = plot_mag_ab


print("Fonctions de tracé OK ✓")
