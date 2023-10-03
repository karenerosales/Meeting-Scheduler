def parse_time(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def format_time(minutes):
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02}:{minutes:02}'

def combine_schedules(person1_busy_schedule, person1_work_hours, person2_busy_schedule, person2_work_hours, duration_of_meeting):
    person1_work_start = parse_time(person1_work_hours[0])
    person1_work_end = parse_time(person1_work_hours[1])
    person2_work_start = parse_time(person2_work_hours[0])
    person2_work_end = parse_time(person2_work_hours[1])

    combined_busy_schedule = [list(map(parse_time, slot)) for slot in (person1_busy_schedule + person2_busy_schedule)]

    available_start = max(person1_work_start, person2_work_start)
    available_end = min(person1_work_end, person2_work_end)
    available_slots = [[available_start, available_end]]

    for busy_slot in combined_busy_schedule:
        start_time, end_time = busy_slot
        for i in range(len(available_slots)):
            slot_start, slot_end = available_slots[i]

            if start_time < slot_end and end_time > slot_start:
                if start_time > slot_start:
                    available_slots.insert(i, [slot_start, start_time])
                    i += 1
                if end_time < slot_end:
                    available_slots.insert(i + 1, [end_time, slot_end])
                available_slots.pop(i)

    available_slots = [[format_time(slot[0]), format_time(slot[1])] for slot in available_slots if slot[1] - slot[0] >= duration_of_meeting]

    return available_slots

with open('input.txt', 'r') as file:
    input_lines = file.readlines()

person1_busy_schedule = eval(input_lines[0].strip())
person1_work_hours = eval(input_lines[1].strip())
person2_busy_schedule = eval(input_lines[2].strip())
person2_work_hours = eval(input_lines[3].strip())
duration_of_meeting = int(input_lines[4].strip())

available_slots = combine_schedules(person1_busy_schedule, person1_work_hours, person2_busy_schedule, person2_work_hours, duration_of_meeting)

with open('output.txt', 'w') as output_file:
    for slot in available_slots:
        output_file.write(f"{slot[0]} - {slot[1]}\n")
        output_file.write("\n")