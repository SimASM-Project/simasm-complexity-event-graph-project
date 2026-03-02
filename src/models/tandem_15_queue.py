from o2despy.sandbox import Sandbox
from datetime import timedelta
import random


class Tandem15Queue(Sandbox):
    def __init__(self, seed=0, code="Tandem15Queue", capacity=5, iat_mean=1.25, ist_mean=1.0):
        super().__init__(seed, code)
        self.capacity = capacity
        self.iat_mean = iat_mean
        self.ist_mean = ist_mean

        self.queue_count_1 = 0
        self.server_count_1 = 0
        self.queue_count_2 = 0
        self.server_count_2 = 0
        self.queue_count_3 = 0
        self.server_count_3 = 0
        self.queue_count_4 = 0
        self.server_count_4 = 0
        self.queue_count_5 = 0
        self.server_count_5 = 0
        self.queue_count_6 = 0
        self.server_count_6 = 0
        self.queue_count_7 = 0
        self.server_count_7 = 0
        self.queue_count_8 = 0
        self.server_count_8 = 0
        self.queue_count_9 = 0
        self.server_count_9 = 0
        self.queue_count_10 = 0
        self.server_count_10 = 0
        self.queue_count_11 = 0
        self.server_count_11 = 0
        self.queue_count_12 = 0
        self.server_count_12 = 0
        self.queue_count_13 = 0
        self.server_count_13 = 0
        self.queue_count_14 = 0
        self.server_count_14 = 0
        self.queue_count_15 = 0
        self.server_count_15 = 0
        self.load_id_counter = 0
        self.departure_count = 0
        self.in_system = 0

        self._last_event_time = None
        self._area_queue_total = 0.0
        self._area_system = 0.0

        self.schedule(self.arrive, timedelta(hours=random.expovariate(1 / self.iat_mean)))

    def _update_areas(self):
        now = self.clock_time
        if self._last_event_time is not None:
            dt = (now - self._last_event_time).total_seconds() / 3600.0
            if dt > 0:
                self._area_queue_total += (self.queue_count_1 + self.queue_count_2 + self.queue_count_3 + self.queue_count_4 + self.queue_count_5 + self.queue_count_6 + self.queue_count_7 + self.queue_count_8 + self.queue_count_9 + self.queue_count_10 + self.queue_count_11 + self.queue_count_12 + self.queue_count_13 + self.queue_count_14 + self.queue_count_15) * dt
                self._area_system += self.in_system * dt
        self._last_event_time = now

    def arrive(self):
        self._update_areas()
        self.in_system += 1
        self.load_id_counter += 1
        self.queue_count_1 += 1
        self.schedule(self.arrive, timedelta(hours=random.expovariate(1 / self.iat_mean)))
        if self.queue_count_1 > 0 and self.server_count_1 < self.capacity:
            self.schedule(self.start_1, timedelta(hours=0))

    def start_1(self):
        self._update_areas()
        if self.queue_count_1 > 0:
            self.queue_count_1 -= 1
            self.server_count_1 += 1
            self.schedule(self.finish_1, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_1(self):
        self._update_areas()
        if self.server_count_1 > 0:
            self.server_count_1 -= 1
            self.queue_count_2 += 1
        if self.queue_count_1 > 0 and self.server_count_1 < self.capacity:
            self.schedule(self.start_1, timedelta(hours=0))
        if self.queue_count_2 > 0 and self.server_count_2 < self.capacity:
            self.schedule(self.start_2, timedelta(hours=0))

    def start_2(self):
        self._update_areas()
        if self.queue_count_2 > 0:
            self.queue_count_2 -= 1
            self.server_count_2 += 1
            self.schedule(self.finish_2, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_2(self):
        self._update_areas()
        if self.server_count_2 > 0:
            self.server_count_2 -= 1
            self.queue_count_3 += 1
        if self.queue_count_2 > 0 and self.server_count_2 < self.capacity:
            self.schedule(self.start_2, timedelta(hours=0))
        if self.queue_count_3 > 0 and self.server_count_3 < self.capacity:
            self.schedule(self.start_3, timedelta(hours=0))

    def start_3(self):
        self._update_areas()
        if self.queue_count_3 > 0:
            self.queue_count_3 -= 1
            self.server_count_3 += 1
            self.schedule(self.finish_3, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_3(self):
        self._update_areas()
        if self.server_count_3 > 0:
            self.server_count_3 -= 1
            self.queue_count_4 += 1
        if self.queue_count_3 > 0 and self.server_count_3 < self.capacity:
            self.schedule(self.start_3, timedelta(hours=0))
        if self.queue_count_4 > 0 and self.server_count_4 < self.capacity:
            self.schedule(self.start_4, timedelta(hours=0))

    def start_4(self):
        self._update_areas()
        if self.queue_count_4 > 0:
            self.queue_count_4 -= 1
            self.server_count_4 += 1
            self.schedule(self.finish_4, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_4(self):
        self._update_areas()
        if self.server_count_4 > 0:
            self.server_count_4 -= 1
            self.queue_count_5 += 1
        if self.queue_count_4 > 0 and self.server_count_4 < self.capacity:
            self.schedule(self.start_4, timedelta(hours=0))
        if self.queue_count_5 > 0 and self.server_count_5 < self.capacity:
            self.schedule(self.start_5, timedelta(hours=0))

    def start_5(self):
        self._update_areas()
        if self.queue_count_5 > 0:
            self.queue_count_5 -= 1
            self.server_count_5 += 1
            self.schedule(self.finish_5, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_5(self):
        self._update_areas()
        if self.server_count_5 > 0:
            self.server_count_5 -= 1
            self.queue_count_6 += 1
        if self.queue_count_5 > 0 and self.server_count_5 < self.capacity:
            self.schedule(self.start_5, timedelta(hours=0))
        if self.queue_count_6 > 0 and self.server_count_6 < self.capacity:
            self.schedule(self.start_6, timedelta(hours=0))

    def start_6(self):
        self._update_areas()
        if self.queue_count_6 > 0:
            self.queue_count_6 -= 1
            self.server_count_6 += 1
            self.schedule(self.finish_6, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_6(self):
        self._update_areas()
        if self.server_count_6 > 0:
            self.server_count_6 -= 1
            self.queue_count_7 += 1
        if self.queue_count_6 > 0 and self.server_count_6 < self.capacity:
            self.schedule(self.start_6, timedelta(hours=0))
        if self.queue_count_7 > 0 and self.server_count_7 < self.capacity:
            self.schedule(self.start_7, timedelta(hours=0))

    def start_7(self):
        self._update_areas()
        if self.queue_count_7 > 0:
            self.queue_count_7 -= 1
            self.server_count_7 += 1
            self.schedule(self.finish_7, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_7(self):
        self._update_areas()
        if self.server_count_7 > 0:
            self.server_count_7 -= 1
            self.queue_count_8 += 1
        if self.queue_count_7 > 0 and self.server_count_7 < self.capacity:
            self.schedule(self.start_7, timedelta(hours=0))
        if self.queue_count_8 > 0 and self.server_count_8 < self.capacity:
            self.schedule(self.start_8, timedelta(hours=0))

    def start_8(self):
        self._update_areas()
        if self.queue_count_8 > 0:
            self.queue_count_8 -= 1
            self.server_count_8 += 1
            self.schedule(self.finish_8, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_8(self):
        self._update_areas()
        if self.server_count_8 > 0:
            self.server_count_8 -= 1
            self.queue_count_9 += 1
        if self.queue_count_8 > 0 and self.server_count_8 < self.capacity:
            self.schedule(self.start_8, timedelta(hours=0))
        if self.queue_count_9 > 0 and self.server_count_9 < self.capacity:
            self.schedule(self.start_9, timedelta(hours=0))

    def start_9(self):
        self._update_areas()
        if self.queue_count_9 > 0:
            self.queue_count_9 -= 1
            self.server_count_9 += 1
            self.schedule(self.finish_9, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_9(self):
        self._update_areas()
        if self.server_count_9 > 0:
            self.server_count_9 -= 1
            self.queue_count_10 += 1
        if self.queue_count_9 > 0 and self.server_count_9 < self.capacity:
            self.schedule(self.start_9, timedelta(hours=0))
        if self.queue_count_10 > 0 and self.server_count_10 < self.capacity:
            self.schedule(self.start_10, timedelta(hours=0))

    def start_10(self):
        self._update_areas()
        if self.queue_count_10 > 0:
            self.queue_count_10 -= 1
            self.server_count_10 += 1
            self.schedule(self.finish_10, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_10(self):
        self._update_areas()
        if self.server_count_10 > 0:
            self.server_count_10 -= 1
            self.queue_count_11 += 1
        if self.queue_count_10 > 0 and self.server_count_10 < self.capacity:
            self.schedule(self.start_10, timedelta(hours=0))
        if self.queue_count_11 > 0 and self.server_count_11 < self.capacity:
            self.schedule(self.start_11, timedelta(hours=0))

    def start_11(self):
        self._update_areas()
        if self.queue_count_11 > 0:
            self.queue_count_11 -= 1
            self.server_count_11 += 1
            self.schedule(self.finish_11, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_11(self):
        self._update_areas()
        if self.server_count_11 > 0:
            self.server_count_11 -= 1
            self.queue_count_12 += 1
        if self.queue_count_11 > 0 and self.server_count_11 < self.capacity:
            self.schedule(self.start_11, timedelta(hours=0))
        if self.queue_count_12 > 0 and self.server_count_12 < self.capacity:
            self.schedule(self.start_12, timedelta(hours=0))

    def start_12(self):
        self._update_areas()
        if self.queue_count_12 > 0:
            self.queue_count_12 -= 1
            self.server_count_12 += 1
            self.schedule(self.finish_12, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_12(self):
        self._update_areas()
        if self.server_count_12 > 0:
            self.server_count_12 -= 1
            self.queue_count_13 += 1
        if self.queue_count_12 > 0 and self.server_count_12 < self.capacity:
            self.schedule(self.start_12, timedelta(hours=0))
        if self.queue_count_13 > 0 and self.server_count_13 < self.capacity:
            self.schedule(self.start_13, timedelta(hours=0))

    def start_13(self):
        self._update_areas()
        if self.queue_count_13 > 0:
            self.queue_count_13 -= 1
            self.server_count_13 += 1
            self.schedule(self.finish_13, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_13(self):
        self._update_areas()
        if self.server_count_13 > 0:
            self.server_count_13 -= 1
            self.queue_count_14 += 1
        if self.queue_count_13 > 0 and self.server_count_13 < self.capacity:
            self.schedule(self.start_13, timedelta(hours=0))
        if self.queue_count_14 > 0 and self.server_count_14 < self.capacity:
            self.schedule(self.start_14, timedelta(hours=0))

    def start_14(self):
        self._update_areas()
        if self.queue_count_14 > 0:
            self.queue_count_14 -= 1
            self.server_count_14 += 1
            self.schedule(self.finish_14, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_14(self):
        self._update_areas()
        if self.server_count_14 > 0:
            self.server_count_14 -= 1
            self.queue_count_15 += 1
        if self.queue_count_14 > 0 and self.server_count_14 < self.capacity:
            self.schedule(self.start_14, timedelta(hours=0))
        if self.queue_count_15 > 0 and self.server_count_15 < self.capacity:
            self.schedule(self.start_15, timedelta(hours=0))

    def start_15(self):
        self._update_areas()
        if self.queue_count_15 > 0:
            self.queue_count_15 -= 1
            self.server_count_15 += 1
            self.schedule(self.finish_15, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def finish_15(self):
        self._update_areas()
        if self.server_count_15 > 0:
            self.server_count_15 -= 1
        if self.queue_count_15 > 0 and self.server_count_15 < self.capacity:
            self.schedule(self.start_15, timedelta(hours=0))
        self.schedule(self.depart, timedelta(hours=0))

    def depart(self):
        self._update_areas()
        if self.in_system > 0:
            self.in_system -= 1
            self.departure_count += 1
