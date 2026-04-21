from django.conf import settings


class SplitSessionCookieMiddleware:
    """Use separate session cookies for /admin,//dashboard and public site.

    This lets the same browser keep an admin session and a public-site session
    without overwriting each other.
    """

    ADMIN_PREFIXES = ('/admin/', '/dashboard/')
    ADMIN_COOKIE = 'admin_sessionid'
    SITE_COOKIE = 'site_sessionid'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        base_name = settings.SESSION_COOKIE_NAME
        is_admin_area = request.path.startswith(self.ADMIN_PREFIXES)
        target_cookie = self.ADMIN_COOKIE if is_admin_area else self.SITE_COOKIE
        source_value = request.COOKIES.get(target_cookie)

        if source_value:
            request.COOKIES[base_name] = source_value
        else:
            request.COOKIES.pop(base_name, None)

        response = self.get_response(request)
        self._sync_response_cookie(response, target_cookie)
        return response

    def _sync_response_cookie(self, response, target_cookie_name):
        base_name = settings.SESSION_COOKIE_NAME
        if base_name not in response.cookies:
            return

        morsel = response.cookies[base_name]
        max_age = morsel['max-age'] or None
        expires = morsel['expires'] or None
        secure = bool(morsel['secure'])
        httponly = bool(morsel['httponly'])
        samesite = morsel['samesite'] or settings.SESSION_COOKIE_SAMESITE
        is_delete = morsel.value == '' or max_age == '0'

        if is_delete:
            response.delete_cookie(
                target_cookie_name,
                path='/',
                domain=settings.SESSION_COOKIE_DOMAIN,
                samesite=samesite,
            )
        else:
            response.set_cookie(
                target_cookie_name,
                morsel.value,
                max_age=max_age,
                expires=expires,
                path='/',
                domain=settings.SESSION_COOKIE_DOMAIN,
                secure=secure,
                httponly=httponly,
                samesite=samesite,
            )

        try:
            del response.cookies[base_name]
        except KeyError:
            pass
