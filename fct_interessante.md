## Fonction `Create_walls` : Génération des murs aléatoires

Cette fonction est définie dans le classe Board permettant de générer aléatoirement des murs, elle est basée sur l’algorithme de Prim.  

     `def create_walls(self):
        # GENERATING RANDOM WALLS

        def allow_visit(j, i):
            return (
                j not in [0, self.game.height - 1]
                and i not in [0, self.game.width - 1]
                and (j, i)
                not in [to_visit_cood for to_visit_cood, parent_cood in to_visit]
                and (j, i) not in visited_path
            )

        def mark_to_visit(j, i):
            for adj_coord in [(j + 1, i), (j - 1, i), (j, i + 1), (j, i - 1)]:
                if allow_visit(*adj_coord):
                    to_visit.append((adj_coord, (j, i)))

        X, Y = np.meshgrid(np.arange(self.game.width), np.arange(self.game.height))
        self.walls = (X % 2 == 0) | (Y % 2 == 0)

        while True:
            begin_j, begin_i = np.random.randint(
                0, self.game.height
            ), np.random.randint(0, self.game.width)
            if begin_j % 2 and begin_i % 2:
                break
            print(begin_j, begin_i)
        visited_island = {(begin_j, begin_i)}
        visited_path = set()
        to_visit = []
        mark_to_visit(begin_j, begin_i)
        while to_visit:
            (visiting_cood, parent_cood) = to_visit.pop(
                np.random.randint(len(to_visit))
            )
            visiting_j, visiting_i = visiting_cood
            detect_j, detect_i = np.array(visiting_cood) * 2 - np.array(parent_cood)
            visited_path.add(visiting_cood)
            if (detect_j, detect_i) not in visited_island:
                self.walls[detect_j, detect_i] = 0
                self.walls[visiting_j, visiting_i] = 0
            visited_island.add((detect_j, detect_i))
            mark_to_visit(detect_j, detect_i)`

