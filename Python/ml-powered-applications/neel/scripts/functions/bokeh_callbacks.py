# dependencies
from bokeh.models import CustomJS

## calback functions
def checkbox_categorical_filter(src, src_orig): 

    # print(sns_ans)

    return CustomJS(

        args=dict(
            source=src,
            source_orig=src_orig,
            ),
            
        code="""
            
            // initialize
            var primary_id = [];
            var x = [];
            var y = [];
            var post_title = [];
            var question_answered = [];
            var kmeans_cluster = [];

            // initialize
            let selected_categories = this.active
            const arr_src = [source_orig]

            // iterate through each argument source
            arr_src.forEach(src => {

                // iterate through rows of data source and see if each satisfies some constraint
                for (var i = 0; i < src.get_length(); i++){
                    if (selected_categories.includes(parseInt(src.data['kmeans_cluster'][i]))){
                        x.push(src.data['x'][i])
                        y.push(src.data['y'][i])
                        question_answered.push(src.data['question_answered'][i])
                        post_title.push(src.data['Title'][i])
                        kmeans_cluster.push(src.data['kmeans_cluster'][i])
                    }
                }

            });

            // update source
            source.data = {
                'Title': post_title,
                'x': x,
                'y': y,
                'question_answered': question_answered,
                'kmeans_cluster': kmeans_cluster
            }
            
            // source.change.emit();
            return source
    """
    )