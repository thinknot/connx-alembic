from typing import List, Optional

from sqlalchemy import func

from ..flapp.extension import db
from ..model.sources import Energy, Power, PowerType, Site


def get_site_count() -> int:
    sesh = db.new_session()
    return sesh.query(Site).count()


def get_sites_kw_total() -> int:
    sesh = db.new_session()
    kw_sum_result = sesh.query(func.sum(Site.pv_power).label("total")).first().total
    return kw_sum_result / 1000 if kw_sum_result is not None else 0


def get_site_by_name(site_name: str) -> Optional[Site]:
    if not site_name:
        return None

    site_lookup_name = site_name.strip().lower()

    sesh = db.new_session()

    site = (
        sesh.query(Site)
        .options(db.joinedload(Site.project))
        .options(db.joinedload(Site.productions))
        .options(db.joinedload(Site.sources))
        .options(db.joinedload(Site.devices))
        .filter(Site.name == site_lookup_name)
        .first()
    )

    sesh.close()
    return site


def get_latest_sites(lim=10) -> List[Site]:
    sesh = db.new_session()

    sites = (
        sesh.query(Site)
        .options(db.joinedload(Site.project))
        .options(db.joinedload(Site.productions))
        .options(db.joinedload(Site.sources))
        .options(db.joinedload(Site.devices))
        .order_by(Site.created_date.desc())
        .limit(lim)
        .all()
    )

    sesh.close()
    return sites


def lookup_source(source_type: PowerType, site_name) -> Optional[Power]:
    lookup_site = get_site_by_name(site_name)
    sesh = db.new_session()
    src = None
    src = (
        sesh.query(Power)
        .options(db.joinedload(Power.device))
        .filter(Power.site_id == lookup_site.id)
        .filter(Power.source_type == source_type)
        .first()
    )
    sesh.close()
    return src
