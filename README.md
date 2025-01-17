# TinyTimer

The tiniest, simplest, always-visible-on-screen Pomodoro timer designed for hyperfocus on Windows.

TinyTimer was designed me, Devon Saliga, to address my frustrations with traditional Pomodoro clocks: they are too large to raimain always visible on the screen, they are bloated with features, have bad UI, and they fail to encourage movement between work sessions. TinyTimer addresses these issues while sparking joy.

---

## Known Defects (As of 24.01.17):

1. **Occasionally hides behind the Windows taskbar**
   - Suggested Fix: Increase refresh timing or reposition the timer to avoid overlap with the taskbar.

2. **SLOTH TIME shifts above the taskbar if "Start Time" is not clicked**
   - Suggested Fix: Address positioning logic to prevent this behavior during idle states.

3. **Multiple instances can be opened simultaneously**
   - Suggested Fix: Add functionality to restrict launching duplicate instances.

4. **TinyTimer icon not showing**

5. **Blocked by Windows Defender**
   https://stackoverflow.com/questions/48946680/how-to-avoid-the-windows-defender-smartscreen-prevented-an-unrecognized-app-fro/66582477#66582477
   
---

## Feature Requests (As of 24.12.08):

1. **Reset all checks without exiting and reopening**
   - Add a "Reset" button to clear all progress seamlessly.

2. **Enhanced searchability**
   - Make the app searchable under additional terms, such as "TinyTimer," "Timer," and "Tiny Timer."

3. **Log total time worked**
   - Include a feature to track and display cumulative focus time.

4. **Improved SLOTH TIME functionality**
   - Add a 5-minute SLOTH TIME timer countdown to let you know when break is done.
   - Introduce a visually "too-large" optional 1-minute countdown for encouraging lifting between working periods.

---

Feel free to contribute, report issues, or suggest features in the Issues section. Together, let’s make TinyTimer even better!
