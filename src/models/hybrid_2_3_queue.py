from o2despy.sandbox import Sandbox
from datetime import timedelta
import random


class Hybrid23Queue(Sandbox):
    def __init__(self, seed=0, code="Hybrid23Queue", capacity=5, iat_mean=1.25, ist_mean=1.0):
        super().__init__(seed, code)
        self.capacity = capacity
        self.iat_mean = iat_mean
        self.ist_mean = ist_mean

        self.queue_count_1 = 0
        self.server_count_1 = 0
        self.queue_count_2 = 0
        self.server_count_2 = 0
        self.branch_queue_1 = 0
        self.branch_server_1 = 0
        self.part_1_num = 0
        self.branch_queue_2 = 0
        self.branch_server_2 = 0
        self.part_2_num = 0
        self.branch_queue_3 = 0
        self.branch_server_3 = 0
        self.part_3_num = 0
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
                self._area_queue_total += (self.queue_count_1 + self.queue_count_2) * dt
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
        if self.queue_count_2 > 0 and self.server_count_2 < self.capacity:
            self.schedule(self.start_2, timedelta(hours=0))
        self.schedule(self.fork, timedelta(hours=0))

    def fork(self):
        self._update_areas()
        self.branch_queue_1 += 1
        self.branch_queue_2 += 1
        self.branch_queue_3 += 1
        if self.branch_queue_1 > 0 and self.branch_server_1 < self.capacity:
            self.schedule(self.branch_start_1, timedelta(hours=0))
        if self.branch_queue_2 > 0 and self.branch_server_2 < self.capacity:
            self.schedule(self.branch_start_2, timedelta(hours=0))
        if self.branch_queue_3 > 0 and self.branch_server_3 < self.capacity:
            self.schedule(self.branch_start_3, timedelta(hours=0))

    def branch_start_1(self):
        self._update_areas()
        if self.branch_queue_1 > 0:
            self.branch_queue_1 -= 1
            self.branch_server_1 += 1
            self.schedule(self.branch_finish_1, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def branch_finish_1(self):
        self._update_areas()
        if self.branch_server_1 > 0:
            self.branch_server_1 -= 1
            self.part_1_num += 1
        if self.branch_queue_1 > 0 and self.branch_server_1 < self.capacity:
            self.schedule(self.branch_start_1, timedelta(hours=0))
        self.schedule(self.join, timedelta(hours=0))

    def branch_start_2(self):
        self._update_areas()
        if self.branch_queue_2 > 0:
            self.branch_queue_2 -= 1
            self.branch_server_2 += 1
            self.schedule(self.branch_finish_2, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def branch_finish_2(self):
        self._update_areas()
        if self.branch_server_2 > 0:
            self.branch_server_2 -= 1
            self.part_2_num += 1
        if self.branch_queue_2 > 0 and self.branch_server_2 < self.capacity:
            self.schedule(self.branch_start_2, timedelta(hours=0))
        self.schedule(self.join, timedelta(hours=0))

    def branch_start_3(self):
        self._update_areas()
        if self.branch_queue_3 > 0:
            self.branch_queue_3 -= 1
            self.branch_server_3 += 1
            self.schedule(self.branch_finish_3, timedelta(hours=random.expovariate(1 / self.ist_mean)))

    def branch_finish_3(self):
        self._update_areas()
        if self.branch_server_3 > 0:
            self.branch_server_3 -= 1
            self.part_3_num += 1
        if self.branch_queue_3 > 0 and self.branch_server_3 < self.capacity:
            self.schedule(self.branch_start_3, timedelta(hours=0))
        self.schedule(self.join, timedelta(hours=0))

    def join(self):
        self._update_areas()
        if self.part_1_num > 0 and self.part_2_num > 0 and self.part_3_num > 0:
            self.part_1_num -= 1
            self.part_2_num -= 1
            self.part_3_num -= 1
            self.schedule(self.attempt_to_depart, timedelta(hours=0))

    def attempt_to_depart(self):
        self._update_areas()
        if random.random() < 0.5:
            self.queue_count_1 += 1
            if self.queue_count_1 > 0 and self.server_count_1 < self.capacity:
                self.schedule(self.start_1, timedelta(hours=0))
        else:
            self.schedule(self.depart, timedelta(hours=0))

    def depart(self):
        self._update_areas()
        if self.in_system > 0:
            self.in_system -= 1
            self.departure_count += 1
