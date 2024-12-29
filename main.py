import sys
import parser
import argparse

EPS = 1e-9

def parse_command_line():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename", help="lillabu file to be analyzed")
    argparser.add_argument("-v", "--verbose", action="store_true", \
            help="extra logging", default=False)
    return argparser.parse_args()

def parse_input_file_or_die(filename : str):
    try:
        with open(filename) as file:
            input_data = parser.parse(file.read())
            if not input_data:
                raise RuntimeError("Some shit happen...")
            return input_data
    except RuntimeError as e:
        print("RUNTIME ERROR:", e)
        sys.exit(1)
    except FileNotFoundError:
        print("RUNTIME ERROR: Invalid file name \'" + args.filename + "\'", \
            sep='')
        sys.exit(1)

def check_data_info_or_die(data_info):
    suicide = False
    for idx, data_entry in zip(range(len(data_info)), data_info):
        if not type(data_entry) is parser.DataUnit:
            print("Wow, dude, data entry has wrong type", type(data_entry))
            suicide = True
        if not data_entry.type in ['L1', 'L2', 'L3', 'L4', 'T4', 'T8', 'B1']:
            print(f"{idx}th data entry has invalid type {data_entry.type}")
            suicide = True
        if abs(data_entry.count - float(int(data_entry.count))) >= EPS:
            print(f"{idx}th data entry has non-integer count value")
            suicide = True
        if data_entry.count < 0:
            print(f"{idx}th data entry has negative count value")
            suicide = True

    if suicide:
        sys.exit(1)

def check_route_info_or_die(route_info):
    suicide = False

    if abs(route_info[0].x) >= EPS or abs(route_info[0].y) >= EPS:
        print("Route must start at (0, 0)")
        suicide = True

    for idx, route_entry in zip(range(len(route_info)), route_info):
        if not type(route_entry) is parser.RouteUnit:
            print("Wow, dude, route entry has wrong type", type(route_entry))
            suicide = True

    if suicide:
        sys.exit(1)

def check_order_info_or_die(order_info):
    suicide = False

    for idx, order_entry in zip(range(len(order_info)), order_info):
        if not type(order_entry) is parser.OrderUnit:
            print("Wow, dude, route entry has wrong type", type(route_entry))
            suicide = True
        if not order_entry.type in ['L1', 'L2', 'L3', 'L4', 'T4', 'T8', 'B1']:
            print(f"{idx}th order entry has invalid type {data_entry.type}")
            suicide = True
        if not order_entry.dir in [-1, 0, 1]:
            print(f"{idx}th order entry has invalid direction {order_entry.dir}");
            suicide = True

    if suicide:
        sys.exit(1)

def check_blocks_balance_or_die(data_info, order_info):
    for block in ['L1', 'L2', 'L3', 'L4', 'T4', 'T8', 'B1']:
        used = sum(order_entry.type == block for order_entry in order_info)
        available = int(sum(data_entry.count for data_entry in data_info if
                data_entry.type == block))

        if used > available:
            print(f"Overuse of block {block}, used {used}, but available only {available}")
            sys.exit(1)

def check_closed_loop_or_die(order_info):
    for order_entry in order_info:
        pass # TODO: Implement me please

def estimate_cost(data_info, order_info, route_info):
    pass # TODO: Implement me please

if __name__ == "__main__":
    cmd_args = parse_command_line()
    data_info, route_info, order_info = \
        parse_input_file_or_die(cmd_args.filename)

    if cmd_args.verbose:
        print(*data_info, sep='\n')
        print(*order_info, sep='\n')
        if route_info:
            print(*route_info, sep='\n')

    if order_info is None:
        check_order_only = False
    else:
        check_order_only = True

    check_data_info_or_die(data_info)
    check_route_info_or_die(route_info)
    if check_order_only:
        check_order_info_or_die(order_info)
        check_blocks_balance_or_die(data_info, order_info)
        check_closed_loop_or_die(order_info)
