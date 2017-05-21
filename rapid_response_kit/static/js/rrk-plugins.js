(function(window, $) {
    // Listen for the jQuery ready event on the document
    $(function() {
        var $form = $(".form"),
            $say = $("#voice, #language"),
            languages;

        function setLanguages(voices) {
            var $voiceEngine = $("#voice-engine"),
                $voiceLanguage = $("#voice-language"),
                s = '<select id="voice-language" name="voice-language" class="form-control">',
                selectedEngine = $voiceEngine.val(),
                selected = "";

            for (var i = 0, l = voices[selectedEngine].length; i < l; i++) {
                selected = (voices[selectedEngine][i].
                    default === true) ? "selected " : "";
                s += "<option " + selected + "value=\"" + voices[selectedEngine][i].value + "\">" + voices[selectedEngine][i].name + "</option>";
            }

            s += "</select>";

            $voiceLanguage.replaceWith(s);
        }

        // Get the list of available languages.
        $.ajax({
            type: "GET",
            url: "/utils/language",
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        }).done(function (data) {
            languages = data;
            setLanguages(languages);
        });

        if ($say.length > 0) {
            $say.hide();

            $form.on("change", "#method", function() {
                var method = $(this).val();

                if(method === "voice") {
                    $say.show();
                    setLanguages(languages);
                }
                else {
                    $say.hide();
                }
            });
        }

        $form.on("change", "#voice-engine", function() {
           setLanguages(languages);
        });

    });
}(window, window.jQuery));
