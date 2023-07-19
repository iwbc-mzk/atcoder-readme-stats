RANK_ICON = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-crown" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 6l4 6l5 -4l-2 10h-14l-2 -10l5 4z"></path></svg>'
HIGHEST_RATING = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-mountain" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M3 20h18l-6.921 -14.612a2.3 2.3 0 0 0 -4.158 0l-6.921 14.612z"></path><path d="M7.5 11l2 2.5l2.5 -2.5l2 3l2.5 -2"></path></svg>'
RATED_MATCHES = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-award" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 9m-6 0a6 6 0 1 0 12 0a6 6 0 1 0 -12 0"></path><path d="M12 15l3.4 5.89l1.598 -3.233l3.598 .232l-3.4 -5.889"></path><path d="M6.802 12l-3.4 5.89l3.598 -.233l1.598 3.232l3.4 -5.889"></path></svg>'
LAST_COMPETED_ICON = '<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-calendar-time" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M11.795 21h-6.795a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v4"></path><path d="M18 18m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"></path><path d="M15 3v4"></path><path d="M7 3v4"></path><path d="M3 11h16"></path><path d="M18 16.496v1.504l1 1"></path></svg>'

ICON = {
    "rank": RANK_ICON,
    "highest_rating": HIGHEST_RATING,
    "rated_matches": RATED_MATCHES,
    "last_competed": LAST_COMPETED_ICON,
}


def get_icon(name: str) -> str:
    return ICON.get(name, "")
