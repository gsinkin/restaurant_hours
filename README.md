Open/Close hours
================

Open/close time parsing for businesses.

Known limitations
=================

Parses a 12hr clock, not 24hr

Not scrubbing inputs.

Example Usage
=============

```
from datetime import datetime
from restaurant_hours import find_open_restaurants

now = datetime.now()
find_open_restaurants("example.csv", now)
```
