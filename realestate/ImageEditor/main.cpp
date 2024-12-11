#include <opencv2/opencv.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <image_path>" << std::endl;
        return -1;
    }

    std::string image_path = argv[1];
    cv::Mat image = cv::imread(image_path);


    // Фільтруємо зображення
    cv::Mat yellow_image = image.clone();
    for (int y = 0; y < yellow_image.rows; y++) {
        for (int x = 0; x < yellow_image.cols; x++) {
            cv::Vec3b& color = yellow_image.at<cv::Vec3b>(y, x);
            if (color[0] > 200) {
                color[0] = std::min(255, static_cast<int>(color[0] * 1.3));
            }
            if (color[1] > 200) {
                color[1] = std::min(255, static_cast<int>(color[1] * 1.3));;
            }
            if (color[2] > 200) {
                color[2] = std::min(255, static_cast<int>(color[2] * 1.3));;
            }
        }
    }

    //зберігаємо зображення
    cv::imwrite(image_path, yellow_image);

    return 0;
}
