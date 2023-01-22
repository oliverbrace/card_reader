<a name="readme-top"></a>

<br />
<div align="center">

  <h3 align="center">Oliver John Brace</h3>

  <p align="center">
    YuGiHo Card reader
  </p>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

This project was created to help me increase my Python programming skills, while also providing a useful tool for selling my YuGiHo playing cards. The application utilizes OpenCV and pytesseract to detect and read the text from the cards, while also looking up the appropriate pricing information online. This enables an automated process of organizing and pricing my collection without manually having to check each card.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

- [OpenCV](https://opencv.org/)

- [pytesseract](https://pypi.org/project/pytesseract/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Install the necessary packages and libraries as outlined in the `req.txt` file. Additionally, you may need to install other packages or dependencies depending on your operating system.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

Install packages in `requirements.txt`

```sh
pip install -r req.txt
```

<p align="right">(<a href="#readme top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

This application can be used to quickly and easily organize and price YuGiHo card collections.

To use the application, follow the steps below:

1. Place a card in front of the camera.
2. The application will detect the card and use pytesseract to read the text.
3. A search will be conducted to find the best match of the found text.
4. Using the match, the application will look up the price of the card.
5. The card's information will be added to a CSV file.

<p align=" right">(<a href="#readme-top">back to top</a>)</p>
