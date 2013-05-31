from libLLE57 import LLE57
import time

treppe = LLE57()

treppe.cmd_set_time()
print treppe.send(True)
time.sleep(5)

treppe.flush()
treppe.cmd_set_conserve_font()
treppe.cmd_set_conserve_text()
print treppe.send(True)
time.sleep(5)

treppe.flush()
treppe.cmd_set_text("Hallo Welt")
print treppe.send(True)
