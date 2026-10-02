from src.learning.learning import Learning
from src.library.result.result_make import Result

def main():

    result = Result()

    learning = Learning(0)
    train_acc = learning.learning()

    learning = Learning(1)
    test_acc = learning.learning()

    acc_list = train_acc + test_acc
    
    result.save_accuracy(acc_list)
    result.save_config()
    result.save_data()


if __name__ == "__main__":
    main()