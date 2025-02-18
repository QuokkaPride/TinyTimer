# TinyTimer

The tiniest, simplest, always-visible-on-screen Pomodoro timer designed for hyperfocus on Windows.

TinyTimer was designed by me, **Devon Saliga**, to address my frustrations with traditional Pomodoro clocks: they are too large to remain always visible on the screen, bloated with unnecessary features, and have poor UI. TinyTimer solves these issues while sparking joy.

---

## Known Defects (As of 24.02.18):

1. **Occasionally hides behind the Windows taskbar**  
   - **Suggested Fix:** Increase refresh timing or reposition the timer to avoid overlap with the taskbar or put slightly above taskbar. 

2. **SLOTH TIME shifts above the taskbar if "Start Time" is not clicked**  
   - **Suggested Fix:** Adjust positioning logic to prevent this behavior during idle states.

3. **Multiple instances can be opened simultaneously**  
   - **Suggested Fix:** Add functionality to restrict launching duplicate instances.

4. **TinyTimer icon not showing** *(Needs investigation)*  

5. **Blocked by Windows Defender**  
   - Potential workaround: [Avoid Windows Defender SmartScreen block](https://stackoverflow.com/questions/48946680/how-to-avoid-the-windows-defender-smartscreen-prevented-an-unrecognized-app-fro/66582477#66582477).

---

## Feature Requests (As of 24.02.18):

1. **Reset all checks without exiting and reopening**  
   - Add a "Reset" button to clear all progress seamlessly.

2. **Enhanced searchability**  
   - Make the app searchable under additional terms, such as `"TinyTimer"`, `"Timer"`, and `"Tiny Timer"`.

3. **Log total time worked**  
   - Include a feature to track and display cumulative focus time.

4. **Improved SLOTH TIME functionality**  
   - Add a **5-minute countdown** timer for SLOTH TIME to indicate when the break is over.  
   - Introduce an **optional, exaggeratedly large 1-minute countdown** to encourage movement between work periods.

---

### 🛠 Contribute  
Feel free to **report issues**, **suggest features**, or **contribute** via the [Issues section](https://github.com/YOUR_REPO/issues).  
Together, let’s make TinyTimer even better! 🚀
