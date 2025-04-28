def estimatePrice(mileage: int):
    t0 = 0
    t1 = 0
    try:
        with open("thetas.txt", "r") as file:
            line = file.readline()
            thetas = line.split(",")
            for theta in thetas:
                tmp = theta.split(":")
                if "t0" in tmp[0]:
                    t0 = float(tmp[1])
                elif "t1" in tmp[0]:
                    t1 = float(tmp[1])
    except Exception as e:
        print(f"Uninitialized thetas: {e}")
    return t0 + t1 * mileage


def main():
    try:
        print("You want to estimate your car by mileage ? You are in \
the right place !")

        mileage = int(input("Enter a mileage for a honest price : "))
        result = estimatePrice(mileage)

        print(f"And voila ! Your car cost {round(result, 2)}$.")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
