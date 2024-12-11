#include <opencv2/opencv.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <image_path>" << std::endl;
        return -1;
    }

    std::string image_path = argv[1];
    cv::Mat image = cv::imread(image_path);

    if (image.empty()) {
        std::cerr << "Error: Could not open or find the image." << std::endl;
        return -1;
    }

    // Змінюємо кольори (додаємо жовтий відтінок)
    cv::Mat yellow_image = image.clone();
    for (int y = 0; y < yellow_image.rows; y++) {
        for (int x = 0; x < yellow_image.cols; x++) {
            cv::Vec3b& color = yellow_image.at<cv::Vec3b>(y, x);
            color[0] = std::min(255, color[0] + 30); // Blue channel
            color[2] = std::min(255, color[2] + 30); // Red channel
        }
    }

    cv::imwrite(image_path, yellow_image);
    std::cout << "Image processed and saved successfully." << std::endl;

    return 0;
}
