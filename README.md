# oscarmureti.github.io

Public site for the Oscar Games puzzle apps. Deliberately separate from the
private game source repo — this exists only to serve things the app stores and
ad networks require to be publicly reachable:

| File | Why it exists |
|---|---|
| `app-ads.txt` | Ad networks verify authorised sellers by fetching this from the developer website's **root**. It must stay at the domain root, which is why this is a user-pages repo rather than a project page. |
| `privacy.html` | Both stores reject an ad-supported app without a reachable privacy policy. |
| `support.html` | Apple requires a Support URL for every app. |

Served at <https://oscarmureti.github.io>.

`.nojekyll` is present so GitHub Pages serves `app-ads.txt` verbatim instead of
letting Jekyll drop it.
