import random
import matplotlib

from typing import List, Dict, Any
from enum import Enum

# Overall datastructure where all simulated data is stored
data_dict: Dict = {}

""" Setting the boundaries of the simulation """
num_sats: int = 500
num_seconds: int = 3000
# The longitude at which to loop
long_loop: int = 180
# The percentage change in longitude per step
step_amount: float = 0.001

""" Setting the relative frequencies of each sat type and creating their bins"""
freq_of_maneuver_sats = 10
freq_of_stray_sats = 5
freq_of_stationary_sats = 100 - (freq_of_maneuver_sats + freq_of_stray_sats)


class SatType(Enum):
    stationary = 1
    stray = 2
    maneuvering = 3

class Sat:
    id: int
    longs: List[float]
    type: SatType
    increasing: bool | None = None

    def __init__(self, p_id, p_longs, p_type):
        self.id = p_id
        self.longs = p_longs
        self.type = p_type

        if self.type == SatType.stray:
            temp_choice: int = random.randint(0, 1)
            self.increasing = True if temp_choice else False


def gen_unique_sat_id(p_sat_dict: Dict) -> int:
    sat_id: int = random.randint(0, 10000)
    return_id = sat_id if sat_id not in p_sat_dict else gen_unique_sat_id(p_sat_dict)

    return return_id


def initialize_sat_dict(p_num_sats) -> Dict:
    global freq_of_stationary_sats, freq_of_maneuver_sats, freq_of_stray_sats

    sat_dict: dict = {}

    for j in range(0, p_num_sats):

        type_disc = random.randint(1, 100)

        # Generate random sat id and starting longitude for each satellite if it's the first run, update track with new point otherwise
        sat_id: int = gen_unique_sat_id(sat_dict)
        sat_long: float = random.randint(1, 180) + random.random()
        sat_type: SatType = SatType.stationary
        if type_disc >= 1 and type_disc < freq_of_stationary_sats:
            sat_type = SatType.stationary
        elif type_disc >= freq_of_stationary_sats and type_disc < 100-freq_of_maneuver_sats:
            sat_type = SatType.stray
        elif type_disc >= 100-freq_of_maneuver_sats and type_disc <= 100:
            sat_type = SatType.maneuvering
        else:
            print('Chosen sat type is none of the above???')
            raise ValueError('No valid sat type chosen')

        temp_sat = Sat(sat_id, [sat_long], sat_type)

        sat_dict.update({sat_id: temp_sat})
    return sat_dict


def apply_perturbation(p_sat: Sat, p_step: float) -> Sat:
    temp_sat = p_sat

    # 1. Stationary satellites move plus or minus step_amount per step, randomly
    if p_sat.type == SatType.stationary:
        temp_choice: int = random.randint(0, 1)
        increment = 1+p_step if temp_choice else (1-p_step)

        last_long = temp_sat.longs[len(temp_sat.longs)-1]
        curr_long = last_long*increment

        temp_sat.longs.append(curr_long)

        return temp_sat

    # 2.  Stray satellites only move in their chosen direction at step_amount per iteration
    elif p_sat.type == SatType.stray:
        temp_sat = p_sat

        increment = 1+p_step if temp_sat.increasing else (1-p_step)

        last_long = temp_sat.longs[len(temp_sat.longs) - 1]
        curr_long = last_long * increment

        temp_sat.longs.append(curr_long)

        return temp_sat


    # 3. Maneuver - TBD
    elif p_sat.type == SatType.maneuvering:
        # TODO: Implement maneuver math
        return p_sat

if __name__ == "__main__":
    # For each time stamp, add a little bit to the longitude of each satellite, looping at
    for i in range(0, num_seconds):
        print(f'Starting iteration #{i+1}')
        if i == 0:
            """ 1. For the first pass, just generate initial longs and sat ids """
            sat_dict: dict = initialize_sat_dict(num_sats)
            data_dict[i] = sat_dict
        else:
            """ 2. For all other loops, check the type for each satellite then apply the correct perturbation """
            # Copy last dict
            current_sat_dict = data_dict[i-1]
            # Apply perturbations
            for sat_id in current_sat_dict:
                current_sat_dict[sat_id] = apply_perturbation(current_sat_dict[sat_id], step_amount)

            # Update overall data dict with new satellites
            data_dict.update({i: current_sat_dict})

        pass