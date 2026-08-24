#!/usr/bin/env bash
# Manual reminder script — actually disable Wi-Fi/networking before running this.
# There is no way to fully automate "no internet" from inside the container,
# so this is a checklist, not a guarantee.
set -euo pipefail

echo "=== OFFLINE TEST CHECKLIST ==="
echo "1. Physically disable Wi-Fi / unplug ethernet now."
echo "2. Run: docker load -i sih26146-bitcoin-intel.tar"
echo "3. Run: docker run -p 8501:8501 sih26146-bitcoin-intel"
echo "4. Open http://localhost:8501 — full flow (upload -> process -> alerts -> graph)"
echo "   must work with ZERO errors in the browser console or terminal."
echo "5. If Pyvis graph renders blank: check cdn_resources='local' in dashboard/app.py."
echo "6. Re-enable networking only after this passes."
