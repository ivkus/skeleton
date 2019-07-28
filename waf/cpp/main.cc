// 基本的mutex/condition_variable的使用

#include <iostream>
#include <thread>
#include <chrono>
#include <mutex>
#include <vector>
#include <condition_variable>
#include <queue>
#include <functional>
#include <map>
#include <atomic>

static std::mutex gs_mtx;
static std::queue<std::function<void()>> gs_queue;
static std::condition_variable cv;

int main()
{
    bool stop = false;
    std::vector<std::thread> threads;

    // 创建5个线程
    for (int i = 0; i < 5; ++i)
    {
        threads.emplace_back([&stop]() {
            while (true)
            {
                std::function<void()> f;
                {
                    // 作用域要包起来，这样f在执行的时候就不占用mutex了
                    std::unique_lock<std::mutex> lock{ gs_mtx };
                    cv.wait(lock, [&stop]() {
                        return !gs_queue.empty() || stop;
                    });
                    // wait的时候会自动释放gs_mtx，唤醒的时候自动重新获取gs_mtx
                    if (stop)
                    {
                        std::cout << std::this_thread::get_id() << " got quit" << std::endl;
                        break; // break就跳出循环，代表线程结束了
                    }
                    f = std::move(gs_queue.front());
                    gs_queue.pop();
                }
                f();
            }
        });
    }

    while (true)
    {
        char c;
        std::cin >> c;
        if (c == 'q')
        {
            std::cout << "got q in main thread" << std::endl;
            stop = true;
            cv.notify_all(); // 唤醒所有的线程，结束程序
            break;
        }
        else
        {
            std::unique_lock<std::mutex> lock{ gs_mtx };
            // 这里必须要保护一下，入队的时候要记得其他的线程也在操作gs_queue
            gs_queue.push(std::bind([](int x) {
                std::cout << std::this_thread::get_id() << " got " << x << std::endl;
            }, int(c)));
            cv.notify_one();
        }
    }

    for (auto &t : threads)
        t.join(); // 等待其他线程的结束
    return 0;
}
