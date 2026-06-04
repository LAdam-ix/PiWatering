# **Garden Controller Project - PiWatering**

---

## **About**
This project is a **basic backend** designed to control the electronics of a garden watering system. It provides essential functionality for managing valves, monitoring sensors, and saving longtime data for staticstics.

In its current state, the project serves as a foundation for further development, focusing on backend operations and a test web interface.

---

## **Current Features**
- Flask-based backend to handle HTTP requests for garden control (Incomplete).
- Database integration for saving information.
- Simple test web interface for basic interaction.

- **Run with PDM:**
  1. Install dependencies with `pdm install`.
  2. Start the application using `pdm start`.

- **Run with Included Virtual Environment:**

  **(NON STANDART INCLUDED EXTRA FOR SEMINAR PROJECT)**
  1. Use the included `.venv` directory:
     - Navigate to the project root.
     - Run the application with `.venv/bin/python3 src/piwatering/app.py`.

---

## **Future Upgrades - TODO List**
- [ ] Maybe replace Flask with a advanced backend framework (Probably django to learn it).
- [ ] Add management endpoints for components.
- [ ] Implement configuration saving/loading endpoints.
- [ ] Remove the test website.
- [ ] Develop a frontend application.

