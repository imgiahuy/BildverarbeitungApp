Diese Python Projekt ist ein kleines Tool, um Bilder zu bearbeiten. 

Funktionen :

- Bildhelligkeit erhöhen/reduzieren
- Kantenerkennung (Canny Algorithm)
- Kreis-Erkennung (Hough Circle Algorithm)
- Undo Manager
- Bild laden
- Bild speichern
- Vorschaubereich 
- Exit

Achtung !!! :

Bei Hough Circle Algorithm habe ich OpenCV HoughCircle() Methode genutzt, da mit traditionellen Algorithm (3D Array Parameterraum) wird es sehr ineffizient (Zeit und Memory) ist. Obwohl durch Testen habe ich erkennt, dass mit echte Algorithm besseres Ergebnis ergibt aber der Kosten ist zu teuer. Die Implementierung des Algorithm habe ich auch in diesem Datei : HoughCircle.py und UsingTheAlgorithm.py

Mit dem HoughCircle() wir koennen das Ergebnis verbessern durch der Einstellung des maximal Radius Paramater in final_0.py

GUI habe ich einfach mit Tkinter und PIL gebaut.
Tkinter fuer GUI und PIL fuer bessere Integration zwischen OpenCV und Tkinter. 