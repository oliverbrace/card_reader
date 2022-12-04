    def extract_card_colour(self):
        if self.edge_method is not None:
            if self.edge_method == "HSV":
                colour = [247 / 2, 7 * 255 / 100, 45 * 255 / 100]
            elif self.edge_method == "RGB":
                colour = [106, 104, 115]
            elif self.edge_method == "LAB":
                colour = [46 * 255 / 100, 2 + 128, -4 + 128]

            mask = edge_mask(
                self.original_image, colour, edge_method=self.edge_method, distance=40
            )
        else:
            mask = simple_edge_mask(self.original_image)

        return apply_mask(self.original_image, mask)