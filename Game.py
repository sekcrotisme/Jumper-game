            self._map.create_rand_food()

        if self._pause:
            return

        episode_end, learn_end = self._solver.train()

        if episode_end:
            self._reset()

        return learn_end

    def _game_main_normal(self):
        if not self._map.has_food():
            self._map.create_rand_food()

        if self._pause or self._is_episode_end():
            return

        self._update_direc(self._solver.next_direc())

        if self._conf.mode == GameMode.NORMAL and self._snake.direc_next != Direc.NONE:
            self._write_logs()

        self._snake.move()

        if self._is_episode_end():
            self._write_logs()  # Write the last step

    def _plot_history(self):
        self._solver.plot()

    def _update_direc(self, new_direc):
        self._snake.direc_next = new_direc
        if self._pause:
            self._snake.move()

    def _toggle_pause(self):
        self._pause = not self._pause

    def _is_episode_end(self):
        return self._snake.dead or self._map.is_full()

    def _reset(self):
        self._snake.reset()
        self._episode += 1

    def _on_exit(self):
        if self._log_file:
            self._log_file.close()
        if self._solver:
            self._solver.close()

    def _init_log_file(self):
        try:
            os.makedirs("logs")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            self._log_file = None
            self._log_file = open("logs/snake.log", "w", encoding="utf-8")
        except FileNotFoundError:
            if self._log_file:
                self._log_file.close()

    def _write_logs(self):
        self._log_file.write(
            f"[ Episode {self._episode} / Step {self._snake.steps} ]\n"
        )
        for i in range(self._map.num_rows):
            for j in range(self._map.num_cols):
                pos = Pos(i, j)
                t = self._map.point(pos).type
                if t == PointType.EMPTY:
                    self._log_file.write("  ")
                elif t == PointType.WALL:
                    self._log_file.write("# ")
                elif t == PointType.FOOD:
                    self._log_file.write("F ")
                elif (
                    t == PointType.HEAD_L
                    or t == PointType.HEAD_U
                    or t == PointType.HEAD_R
                    or t == PointType.HEAD_D
                ):
                    self._log_file.write("H ")
                elif pos == self._snake.tail():
                    self._log_file.write("T ")
                else:
                    self._log_file.write("B ")
            self._log_file.write("\n")
        self._log_file.write(
            f"[ last/next direc: {self._snake.direc}/{self._snake.direc_next} ]\n"
        )
        self._log_file.write("\n")
