from math import fsum
from tqdm import tqdm
import matplotlib.pyplot as plt


class DataSet:

    def __init__(self, title):
        self.data = []  # [(x1,y1 ), (x2, y2) ... (xn, yn)]
        self.dataNorm = []
        self.cost_history = []
        self.theta0 = 0
        self.theta1 = 0

        with open(title, "r") as file:
            lines = file.readlines()
        for line in lines[1:]:
            if ',' in line:
                x, y = line.strip().split(',')
                self.data.append((int(x), int(y)))
        self.__x_max = max([x for x, y in self.data])
        self.__y_max = max([y for x, y in self.data])
        self.dataNorm = [
            (self.__normValue(x, self.__x_max),
             self.__normValue(y, self.__y_max)) for x, y in self.data]

    def __saveThetas(self):
        t0, t1 = self.__denormalizeThetas()
        with open("thetas.txt", 'w') as file:
            file.write(f"t0:{t0},t1:{t1}")

    def getMaxs(self):
        return self.__x_max, self.__y_max

    def __normValue(self, value, max):
        return value / max

    def __unnormValue(self, value, max):
        return value * max

    def __denormalizeThetas(self):
        # denormalize theta1
        tmpT1 = self.theta1 * self.__y_max / self.__x_max

        # denormalize theta0
        tmpT0 = self.theta0 * self.__y_max

        return tmpT0, tmpT1

    def getCost(self):
        cost = fsum([(y - self.estimatePrice(x)) ** 2
                     for x, y in self.dataNorm])
        cost /= len(self.data)
        return cost

    def estimatePrice(self, mileage):
        return self.theta0 + self.theta1 * mileage

    def gradient(self, learningRate=0.01, iteration=20000):
        tmpT0 = 0
        tmpT1 = 0
        size = len(self.data)
        cost = -1

        loop = tqdm(range(iteration))
        for i in loop:

            cost = self.getCost()
            self.cost_history.append(cost)

            if (i % 100 == 0):
                loop.set_description(f"cost : {cost}")

            tmpT0 = fsum(
                [self.estimatePrice(x_i) - y_i
                 for x_i, y_i in self.dataNorm])
            tmpT1 = fsum(
                [(self.estimatePrice(x_i) - y_i) * x_i
                 for x_i, y_i in self.dataNorm])

            self.theta0 -= learningRate * (tmpT0 / size)
            self.theta1 -= learningRate * (tmpT1 / size)

        self.__saveThetas()


def main():
    data = DataSet("data.csv")
    data.gradient()

    unNorm_max_x, unNorm_max_y = data.getMaxs()

    x_min = min([x for x, y in data.data])
    x_max = max([x for x, y in data.data])

    y_min = data.estimatePrice(x_min / unNorm_max_x) * unNorm_max_y
    y_max = data.estimatePrice(x_max / unNorm_max_x) * unNorm_max_y

    plt.figure("Linear regression", figsize=(10, 4))

    # Print data, regression
    plt.subplot(121)
    plt.scatter([x for x, y in data.data], [y for x, y in data.data],
                alpha=0.5)
    plt.axline((x_min, y_min), (x_max, y_max), c="r")
    plt.ylabel("Price")
    plt.xlabel("Mileages")

    # Print cost history
    plt.subplot(122)
    plt.plot(data.cost_history, c='b')
    plt.ylabel("Cost")
    plt.xlabel("Iterations")

    plt.show()


if __name__ == "__main__":
    main()
